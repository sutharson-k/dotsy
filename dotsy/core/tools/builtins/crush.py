"""Crush CLI integration for Dotsy.

This module provides integration between Dotsy and Crush CLI, allowing Dotsy to:
1. Use Crush CLI tools via MCP protocol
2. Coordinate with Crush as an autonomous agent
3. Share context and session information
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any

from pydantic import BaseModel, Field

from dotsy.core.tools.base import BaseTool, BaseToolConfig, BaseToolState, InvokeContext, ToolError
from dotsy.core.tools.ui import ToolCallDisplay, ToolResultDisplay
from dotsy.core.types import ToolStreamEvent


class CrushToolState(BaseToolState):
    """State for Crush CLI tools."""


class CrushToolArgs(BaseModel):
    """Base arguments for Crush CLI tools."""

    task: str = Field(default="", description="Task to execute with Crush CLI")


class CrushToolResult(BaseModel):
    """Base result for Crush CLI tools."""

    success: bool
    output: str
    error: str | None = None


class CrushConfig:
    """Configuration for Crush CLI integration."""

    def __init__(
        self,
        config_path: Path | None = None,
        auto_approve_tools: list[str] | None = None,
        disabled_tools: list[str] | None = None,
    ) -> None:
        self.config_path = config_path or self._find_crush_config()
        self.auto_approve_tools = auto_approve_tools or []
        self.disabled_tools = disabled_tools or []

    @classmethod
    def _find_crush_config(cls) -> Path | None:
        """Find Crush configuration file in priority order."""
        candidates = [
            Path.cwd() / ".crush.json",
            Path.cwd() / "crush.json",
            Path.home() / ".config" / "crush" / "crush.json",
        ]
        for path in candidates:
            if path.exists():
                return path
        return None

    def load_config(self) -> dict[str, Any] | None:
        """Load Crush configuration."""
        if not self.config_path or not self.config_path.exists():
            return None
        try:
            with open(self.config_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None


class CrushCLI:
    """Interface to interact with Crush CLI."""

    def __init__(self, config: CrushConfig | None = None) -> None:
        self.config = config or CrushConfig()
        self._crush_path = self._find_crush_executable()

    @classmethod
    def _find_crush_executable(cls) -> str | None:
        """Find Crush CLI executable in PATH."""
        return shutil.which("crush")

    def is_available(self) -> bool:
        """Check if Crush CLI is available."""
        return self._crush_path is not None

    def get_version(self) -> str | None:
        """Get Crush CLI version."""
        if not self.is_available():
            return None
        try:
            result = subprocess.run(
                ["crush", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            return None

    def run_command(
        self,
        args: list[str],
        cwd: Path | None = None,
        timeout: int = 300,
    ) -> tuple[int, str, str]:
        """Run a Crush CLI command.

        Args:
            args: Command line arguments
            cwd: Working directory
            timeout: Timeout in seconds

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        if not self.is_available():
            raise ToolError("Crush CLI is not installed or not in PATH")

        try:
            result = subprocess.run(
                ["crush"] + args,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=timeout,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            raise ToolError("Crush CLI command timed out")
        except FileNotFoundError as e:
            raise ToolError(f"Failed to execute Crush CLI: {e}")

    def get_logs(self, tail: int = 100, follow: bool = False) -> str:
        """Get Crush CLI logs."""
        args = ["logs", "--tail", str(tail)]
        if follow:
            args.append("--follow")
        _, stdout, stderr = self.run_command(args)
        return stdout if not stderr else stderr

    def update_providers(self) -> str:
        """Update Crush CLI providers."""
        _, stdout, stderr = self.run_command(["update-providers"])
        return stdout if not stderr else stderr

    def get_context(self) -> dict[str, Any] | None:
        """Get current Crush context including AGENTS.md if available."""
        agents_file = Path.cwd() / "AGENTS.md"
        if agents_file.exists():
            try:
                return {
                    "agents_md": agents_file.read_text(),
                    "config": self.config.load_config(),
                }
            except OSError:
                pass
        return None


class CrushTool(BaseTool[CrushToolArgs, CrushToolResult, BaseToolConfig, CrushToolState]):
    """Base class for Crush CLI tools."""

    crush_cli = CrushCLI()

    def __init__(
        self,
        config: BaseToolConfig | None = None,
        state: CrushToolState | None = None,
    ) -> None:
        super().__init__(
            config=config or BaseToolConfig(),
            state=state or CrushToolState(),
        )
        if not self.crush_cli.is_available():
            raise ToolError(
                "Crush CLI is not available. Please install it from "
                "https://github.com/charmbracelet/crush"
            )

    async def run(
        self,
        args: CrushToolArgs,
        ctx: InvokeContext | None = None,
    ) -> AsyncGenerator[ToolStreamEvent | CrushToolResult, None]:
        """Run the Crush CLI tool with typed arguments."""
        if not args.task:
            raise ToolError("Task parameter is required")

        tool_call_id = ctx.tool_call_id if ctx else f"{self.get_name()}-001"

        yield ToolStreamEvent(
            tool_name=self.get_name(),
            message=f"Running Crush task: {args.task}",
            tool_call_id=tool_call_id,
        )

        # Run Crush with the task
        returncode, stdout, stderr = self.crush_cli.run_command(
            ["--yolo", args.task],
            timeout=600,
        )

        if returncode != 0:
            raise ToolError(f"Crush CLI failed: {stderr or stdout}")

        yield CrushToolResult(
            success=True,
            output=stdout,
            error=stderr if stderr else None,
        )


class CrushRunTool(CrushTool):
    """Run a task using Crush CLI."""

    TOOL_NAME = "crush_run"
    TOOL_DESCRIPTION = (
        "Execute a task using Crush CLI. Use this to leverage Crush's "
        "capabilities for coding tasks, file operations, and code analysis. "
        "Crush will handle the task and return the result."
    )

    def get_display(self, parameters: dict[str, Any]) -> ToolCallDisplay:
        return ToolCallDisplay(
            summary=f"🔨 Crush Run: {parameters.get('task', 'N/A')}",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            success=True,
            message="Task completed by Crush CLI",
        )


class CrushReadContextTool(CrushTool):
    """Read Crush's project context (AGENTS.md)."""

    TOOL_NAME = "crush_read_context"
    TOOL_DESCRIPTION = (
        "Read the project context from Crush's AGENTS.md file. "
        "This contains project-specific information that Crush uses "
        "for understanding the codebase."
    )

    def get_display(self, parameters: dict[str, Any]) -> ToolCallDisplay:
        return ToolCallDisplay(
            summary="Reading Crush context from AGENTS.md",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            success=True,
            message="Successfully read Crush project context",
        )


class CrushLogsTool(CrushTool):
    """Get Crush CLI logs."""

    TOOL_NAME = "crush_logs"
    TOOL_DESCRIPTION = (
        "Retrieve recent logs from Crush CLI sessions. "
        "Useful for debugging or understanding what Crush has been doing."
    )

    def get_display(self, parameters: dict[str, Any]) -> ToolCallDisplay:
        return ToolCallDisplay(
            summary="Retrieving Crush CLI logs",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            success=True,
            message="Successfully retrieved Crush logs",
        )


class CrushUpdateProvidersTool(CrushTool):
    """Update Crush CLI providers."""

    TOOL_NAME = "crush_update_providers"
    TOOL_DESCRIPTION = (
        "Update the list of available LLM providers in Crush CLI. "
        "This fetches the latest provider configurations."
    )

    def get_display(self, parameters: dict[str, Any]) -> ToolCallDisplay:
        return ToolCallDisplay(
            summary="Updating Crush CLI providers",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            success=True,
            message="Successfully updated Crush CLI providers",
        )


# Export all Crush tools
CRUSH_TOOLS = [
    CrushRunTool,
    CrushReadContextTool,
    CrushLogsTool,
    CrushUpdateProvidersTool,
]


def get_crush_tools() -> list[type[CrushTool]]:
    """Get all available Crush tools."""
    cli = CrushCLI()
    if not cli.is_available():
        return []
    return CRUSH_TOOLS
