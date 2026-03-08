"""Crush CLI integration for Dotsy.

This module provides integration between Dotsy and Crush CLI, allowing Dotsy to:
1. Use Crush CLI tools via MCP protocol
2. Coordinate with Crush as an autonomous agent
3. Share context and session information
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from dotsy.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    InvokeContext,
    ToolError,
)
from dotsy.core.tools.ui import ToolCallDisplay, ToolResultDisplay
from dotsy.core.types import ToolStreamEvent


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


class CrushTool(BaseTool):
    """Base class for Crush CLI tools."""

    crush_cli = CrushCLI()

    def __init__(self, config: BaseToolConfig | None = None) -> None:
        super().__init__(config=config)
        if not self.crush_cli.is_available():
            raise ToolError(
                "Crush CLI is not available. Please install it from "
                "https://github.com/charmbracelet/crush"
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
            title="🔨 Crush Run",
            description=f"Running task with Crush: {parameters.get('task', 'N/A')}",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            title="✅ Crush Complete",
            description="Task completed by Crush CLI",
        )

    async def invoke(
        self,
        parameters: dict[str, Any],
        context: InvokeContext,
    ) -> AsyncGenerator[ToolStreamEvent, None]:
        task = parameters.get("task", "")
        if not task:
            raise ToolError("Task parameter is required")

        # Run Crush with the task
        returncode, stdout, stderr = self.crush_cli.run_command(
            ["--yolo", task],
            timeout=600,
        )

        if returncode != 0:
            raise ToolError(f"Crush CLI failed: {stderr or stdout}")

        yield ToolStreamEvent(
            type="tool_result",
            content={
                "success": True,
                "output": stdout,
                "task": task,
            },
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
            title="📖 Read Crush Context",
            description="Reading project context from AGENTS.md",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            title="✅ Context Retrieved",
            description="Successfully read Crush project context",
        )

    async def invoke(
        self,
        parameters: dict[str, Any],
        context: InvokeContext,
    ) -> AsyncGenerator[ToolStreamEvent, None]:
        ctx = self.crush_cli.get_context()
        if not ctx:
            raise ToolError("No Crush context found (AGENTS.md not found)")

        yield ToolStreamEvent(
            type="tool_result",
            content=ctx,
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
            title="📋 Get Crush Logs",
            description=f"Retrieving last {parameters.get('tail', 100)} log lines",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            title="✅ Logs Retrieved",
            description="Successfully retrieved Crush logs",
        )

    async def invoke(
        self,
        parameters: dict[str, Any],
        context: InvokeContext,
    ) -> AsyncGenerator[ToolStreamEvent, None]:
        tail = parameters.get("tail", 100)
        logs = self.crush_cli.get_logs(tail=tail)

        yield ToolStreamEvent(
            type="tool_result",
            content={
                "logs": logs,
                "lines": tail,
            },
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
            title="🔄 Update Crush Providers",
            description="Updating Crush CLI provider list",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        return ToolResultDisplay(
            title="✅ Providers Updated",
            description="Successfully updated Crush CLI providers",
        )

    async def invoke(
        self,
        parameters: dict[str, Any],
        context: InvokeContext,
    ) -> AsyncGenerator[ToolStreamEvent, None]:
        output = self.crush_cli.update_providers()

        yield ToolStreamEvent(
            type="tool_result",
            content={
                "success": True,
                "output": output,
            },
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
