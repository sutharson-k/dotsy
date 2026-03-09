from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

from rich import print as rprint

from dotsy import __version__
from dotsy.core.agents.models import BuiltinAgentName
from dotsy.core.paths.config_paths import unlock_config_paths
from dotsy.core.trusted_folders import has_trustable_content, trusted_folders_manager
from dotsy.setup.trusted_folders.trust_folder_dialog import (
    TrustDialogQuitException,
    ask_trust_folder,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Dotsy interactive CLI")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "initial_prompt",
        nargs="?",
        metavar="PROMPT",
        help="Initial prompt to start the interactive session with.",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        nargs="?",
        const="",
        metavar="TEXT",
        help="Run in programmatic mode: send prompt, auto-approve all tools, "
        "output response, and exit.",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        metavar="N",
        help="Maximum number of assistant turns "
        "(only applies in programmatic mode with -p).",
    )
    parser.add_argument(
        "--max-price",
        type=float,
        metavar="DOLLARS",
        help="Maximum cost in dollars (only applies in programmatic mode with -p). "
        "Session will be interrupted if cost exceeds this limit.",
    )
    parser.add_argument(
        "--enabled-tools",
        action="append",
        metavar="TOOL",
        help="Enable specific tools. In programmatic mode (-p), this disables "
        "all other tools. "
        "Can use exact names, glob patterns (e.g., 'bash*'), or "
        "regex with 're:' prefix. Can be specified multiple times.",
    )
    parser.add_argument(
        "--output",
        type=str,
        choices=["text", "json", "streaming"],
        default="text",
        help="Output format for programmatic mode (-p): 'text' "
        "for human-readable (default), 'json' for all messages at end, "
        "'streaming' for newline-delimited JSON per message.",
    )
    parser.add_argument(
        "--agent",
        metavar="NAME",
        default=BuiltinAgentName.DEFAULT,
        help="Agent to use (builtin: default, plan, accept-edits, auto-approve, "
        "or custom from ~/.dotsy/agents/NAME.toml)",
    )
    parser.add_argument("--setup", action="store_true", help="Setup API key and exit")
    parser.add_argument(
        "--set-api-key",
        metavar="KEY",
        help="Set API key for the current provider and exit",
    )
    parser.add_argument(
        "--provider",
        metavar="NAME",
        choices=["mistral", "openai", "anthropic", "google", "llamacpp", "ollama"],
        default="mistral",
        help="Provider to set API key for (default: mistral). Use with --set-api-key",
    )
    parser.add_argument(
        "--workdir",
        type=Path,
        metavar="DIR",
        help="Change to this directory before running",
    )
    parser.add_argument(
        "-f", "--file",
        action="append",
        metavar="FILE",
        dest="files",
        help="Attach a file to the initial prompt (can be specified multiple times). "
        "Supports images, PDFs, and text files.",
    )

    continuation_group = parser.add_mutually_exclusive_group()
    continuation_group.add_argument(
        "-c",
        "--continue",
        action="store_true",
        dest="continue_session",
        help="Continue from the most recent saved session",
    )
    continuation_group.add_argument(
        "--resume",
        metavar="SESSION_ID",
        help="Resume a specific session by its ID (supports partial matching)",
    )
    return parser.parse_args()


def check_and_resolve_trusted_folder() -> None:
    try:
        cwd = Path.cwd()
    except FileNotFoundError:
        rprint(
            "[red]Error: Current working directory no longer exists.[/]\n"
            "[yellow]The directory you started dotsy from has been deleted. "
            "Please change to an existing directory and try again, "
            "or use --workdir to specify a working directory.[/]"
        )
        sys.exit(1)

    if not has_trustable_content(cwd) or cwd.resolve() == Path.home().resolve():
        return

    is_folder_trusted = trusted_folders_manager.is_trusted(cwd)

    if is_folder_trusted is not None:
        return

    try:
        is_folder_trusted = ask_trust_folder(cwd)
    except (KeyboardInterrupt, EOFError, TrustDialogQuitException):
        sys.exit(0)
    except Exception as e:
        rprint(f"[yellow]Error showing trust dialog: {e}[/]")
        return

    if is_folder_trusted is True:
        trusted_folders_manager.add_trusted(cwd)
    elif is_folder_trusted is False:
        trusted_folders_manager.add_untrusted(cwd)


def main() -> None:
    args = parse_arguments()

    # Handle --set-api-key option
    if args.set_api_key:
        _handle_set_api_key(args.set_api_key, args.provider)
        sys.exit(0)

    if args.workdir:
        workdir = args.workdir.expanduser().resolve()
        if not workdir.is_dir():
            rprint(
                f"[red]Error: --workdir does not exist or is not a directory: {workdir}[/]"
            )
            sys.exit(1)
        os.chdir(workdir)

    is_interactive = args.prompt is None
    if is_interactive:
        check_and_resolve_trusted_folder()
    unlock_config_paths()

    from dotsy.cli.cli import run_cli

    run_cli(args)


def _handle_set_api_key(api_key: str, provider_name: str) -> None:
    """Set API key for the specified provider."""
    from dotenv import set_key

    from dotsy.core.config import DEFAULT_PROVIDERS
    from dotsy.core.paths.global_paths import GLOBAL_ENV_FILE

    # Find provider config
    provider = None
    for p in DEFAULT_PROVIDERS:
        if p.name == provider_name:
            provider = p
            break

    if not provider:
        rprint(f"[red]Error: Unknown provider '{provider_name}'[/]")
        sys.exit(1)

    if not provider.api_key_env_var:
        rprint(f"[yellow]Warning: {provider_name} does not require an API key[/]")
        return

    # Set in environment for current session
    os.environ[provider.api_key_env_var] = api_key

    # Save to .env file
    try:
        GLOBAL_ENV_FILE.path.parent.mkdir(parents=True, exist_ok=True)
        set_key(GLOBAL_ENV_FILE.path, provider.api_key_env_var, api_key)
        rprint(f"[green]✓ API key saved for {provider_name}![/]")
        rprint(f"[dim]  Stored in: {GLOBAL_ENV_FILE.path}[/]")
        rprint(f"[dim]  Environment variable: {provider.api_key_env_var}[/]")
        rprint("\n[green]You can now run 'dotsy' to start![/]")
    except OSError as e:
        rprint(f"[red]Error saving API key: {e}[/]")
        sys.exit(1)


if __name__ == "__main__":
    main()
