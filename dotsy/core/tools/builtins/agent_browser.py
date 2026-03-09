"""Agent Browser integration for Dotsy.

This module provides browser automation capabilities using agent-browser CLI.
Enables AI agents to navigate websites, interact with elements, and extract content.

Features:
- Navigate to URLs and web pages
- Click, fill, type interactions
- Take screenshots (standard and annotated)
- Extract page content and accessibility trees
- Session management with persistence
- Domain allowlist for security

Security:
- Requires user approval for actions (configurable)
- Domain allowlist prevents unauthorized sites
- Session data can be cleared on exit
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, AsyncGenerator

from pydantic import BaseModel, Field, ValidationError

from dotsy.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    BaseToolState,
    InvokeContext,
    ToolError,
)
from dotsy.core.tools.ui import ToolCallDisplay, ToolResultDisplay, ToolUIData
from dotsy.core.types import ToolStreamEvent


class AgentBrowserConfig(BaseToolConfig):
    """Configuration for agent-browser tool."""

    headless: bool = True
    timeout_seconds: int = 30
    domain_allowlist: list[str] = []
    profile_path: str = ""
    provider: str = "local"  # local, browserbase, browser-use, kernel, ios


class AgentBrowserState(BaseToolState):
    """State for agent-browser tool."""

    current_url: str = ""
    session_id: str = ""


class AgentBrowserArgs(BaseModel):
    """Arguments for agent-browser actions."""

    action: str = Field(
        description="Action to perform: open, snapshot, click, fill, type, screenshot, scroll, etc."
    )
    url: str | None = Field(
        default=None,
        description="URL to navigate to (for 'open' action)",
    )
    element_ref: str | None = Field(
        default=None,
        description="Element reference (e.g., '@e1', '@e2') for click/fill/type",
    )
    text: str | None = Field(
        default=None,
        description="Text to fill or type (for 'fill' or 'type' actions)",
    )
    screenshot_path: str | None = Field(
        default=None,
        description="Path to save screenshot (for 'screenshot' action)",
    )
    wait_for: str | None = Field(
        default=None,
        description="Wait for element/text/URL before proceeding",
    )
    provider: str | None = Field(
        default=None,
        description="Browser provider: local, browserbase, browser-use, kernel, ios",
    )


class AgentBrowserResult(BaseModel):
    """Result from agent-browser action."""

    success: bool
    action: str
    output: str | None = None
    screenshot_path: str | None = None
    snapshot: dict[str, Any] | None = None
    error: str | None = None


class AgentBrowser(
    BaseTool[
        AgentBrowserArgs,
        AgentBrowserResult,
        AgentBrowserConfig,
        AgentBrowserState,
    ],
):
    """Browser automation using agent-browser CLI.

    Navigate websites, interact with elements, take screenshots,
    and extract content for AI-driven web automation.
    """

    TOOL_NAME = "agent_browser"
    TOOL_DESCRIPTION = (
        "Automate browser actions using agent-browser. Use this tool AUTOMATICALLY when users ask to: "
        "open/navigate/visit/go to a website URL, check a web page, take screenshots, click/fill/type on web pages, "
        "or extract content from websites. Examples: 'open amazon.com', 'what do you see on github.com', "
        "'take a screenshot of example.com', 'click the login button'. "
        "Navigate to URLs, click/fill elements, take screenshots, and extract page content. "
        "Requires agent-browser CLI: npm install -g agent-browser"
    )

    def __init__(
        self,
        config: AgentBrowserConfig | None = None,
        state: AgentBrowserState | None = None,
    ) -> None:
        super().__init__(config=config, state=state)
        self._agent_browser_path = self._find_agent_browser()

    @classmethod
    def _find_agent_browser(cls) -> str | None:
        """Find agent-browser CLI in PATH."""
        return shutil.which("agent-browser")

    def is_available(self) -> bool:
        """Check if agent-browser CLI is available."""
        return self._agent_browser_path is not None

    def get_display(self, parameters: dict[str, Any]) -> ToolCallDisplay:
        action = parameters.get("action", "unknown")
        url = parameters.get("url", "")
        return ToolCallDisplay(
            summary=f"Browser: {action} {url or parameters.get('element_ref', '')}",
        )

    def get_result_display(
        self, result: dict[str, Any], parameters: dict[str, Any]
    ) -> ToolResultDisplay:
        success = result.get("success", False)
        action = result.get("action", "action")
        if success:
            return ToolResultDisplay(
                success=True,
                message=f"Browser {action} completed successfully",
            )
        else:
            return ToolResultDisplay(
                success=False,
                message=f"Browser {action} failed: {result.get('error', 'Unknown error')}",
            )

    async def run(
        self,
        args: AgentBrowserArgs,
        ctx: InvokeContext | None = None,
    ) -> AsyncGenerator[ToolStreamEvent | AgentBrowserResult, None]:
        if not self.is_available():
            raise ToolError(
                "agent-browser CLI not found. Install with: npm install -g agent-browser"
            )

        # Validate URL against allowlist
        if args.url and self.config.domain_allowlist:
            if not self._is_url_allowed(args.url):
                raise ToolError(
                    f"URL not in domain allowlist: {args.url}. "
                    f"Allowed: {', '.join(self.config.domain_allowlist)}"
                )

        # Generate tool_call_id if not provided
        tool_call_id = ctx.tool_call_id if ctx else "browser-001"

        yield ToolStreamEvent(
            tool_name=self.TOOL_NAME,
            message=f"Browser: {args.action} {args.url or args.element_ref or ''}",
            tool_call_id=tool_call_id,
        )

        try:
            result = await self._execute_action(args)
            # Yield result as AgentBrowserResult (not ToolStreamEvent)
            yield AgentBrowserResult(
                success=True,
                action=args.action,
                output=result.output,
                screenshot_path=result.screenshot_path,
                snapshot=result.snapshot,
            )
        except subprocess.TimeoutExpired as e:
            raise ToolError(f"Browser action timed out: {e}") from e
        except subprocess.SubprocessError as e:
            raise ToolError(f"Browser command failed: {e}") from e
        except Exception as e:
            raise ToolError(f"Browser action failed: {e}") from e

    def _is_url_allowed(self, url: str) -> bool:
        """Check if URL is in domain allowlist."""
        from urllib.parse import urlparse

        # If allowlist is ['*'] or empty, allow all
        if not self.config.domain_allowlist or self.config.domain_allowlist == ['*']:
            return True

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        for allowed in self.config.domain_allowlist:
            if allowed == '*':
                return True
            if allowed.startswith("*."):
                # Wildcard subdomain
                if domain.endswith(allowed[1:]):
                    return True
            elif domain == allowed.lower():
                return True

        # Always allow localhost
        if "localhost" in domain or "127.0.0.1" in domain:
            return True

        return False

    async def _execute_action(self, args: AgentBrowserArgs) -> AgentBrowserResult:
        """Execute agent-browser action."""
        cmd = [self._agent_browser_path]

        # Add provider if specified
        if args.provider or self.config.provider != "local":
            provider = args.provider or self.config.provider
            cmd.extend(["-p", provider])

        # Add headless/headed flag (explicit, not default)
        if self.config.headless:
            cmd.append("--headless")
        else:
            cmd.append("--headed")  # Explicitly show browser window

        # Add timeout
        cmd.extend(["--timeout", str(self.config.timeout_seconds * 1000)])

        # Add profile path if specified
        if self.config.profile_path:
            cmd.extend(["--profile", self.config.profile_path])

        # Build action command
        match args.action:
            case "open":
                if not args.url:
                    raise ToolError("URL required for 'open' action")
                cmd.extend(["open", args.url])

            case "snapshot":
                cmd.extend(["snapshot", "--json"])
                if args.wait_for:
                    cmd.extend(["--wait-for", args.wait_for])

            case "click":
                if not args.element_ref:
                    raise ToolError("Element ref required for 'click' action")
                cmd.extend(["click", args.element_ref])

            case "fill":
                if not args.element_ref or not args.text:
                    raise ToolError("Element ref and text required for 'fill' action")
                cmd.extend(["fill", args.element_ref, args.text])

            case "type":
                if not args.element_ref or not args.text:
                    raise ToolError("Element ref and text required for 'type' action")
                cmd.extend(["type", args.element_ref, args.text])

            case "screenshot":
                cmd.append("screenshot")
                if args.screenshot_path:
                    cmd.append(args.screenshot_path)
                else:
                    cmd.append("--annotated")

            case "scroll":
                cmd.extend(["scroll", args.element_ref or "page"])

            case "hover":
                if not args.element_ref:
                    raise ToolError("Element ref required for 'hover' action")
                cmd.extend(["hover", args.element_ref])

            case "wait":
                if not args.wait_for:
                    raise ToolError("Wait condition required")
                cmd.extend(["wait", args.wait_for])

            case _:
                raise ToolError(f"Unknown action: {args.action}")

        # Execute command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.config.timeout_seconds,
        )

        if result.returncode != 0:
            return AgentBrowserResult(
                success=False,
                action=args.action,
                error=result.stderr or result.stdout,
            )

        # Parse result based on action
        output = result.stdout.strip()
        snapshot = None

        if args.action == "snapshot":
            try:
                snapshot = json.loads(output)
                output = f"Snapshot captured: {len(snapshot.get('nodes', []))} elements"
            except json.JSONDecodeError:
                pass

        screenshot_path = None
        if args.action == "screenshot" and args.screenshot_path:
            screenshot_path = args.screenshot_path
            output = f"Screenshot saved to: {screenshot_path}"

        return AgentBrowserResult(
            success=True,
            action=args.action,
            output=output,
            screenshot_path=screenshot_path,
            snapshot=snapshot,
        )

    @classmethod
    def get_call_display(cls, event: ToolCallEvent) -> ToolCallDisplay:
        if not isinstance(event.args, AgentBrowserArgs):
            return ToolCallDisplay(summary="Browser action...")
        action = event.args.action
        target = event.args.url or event.args.element_ref or ""
        return ToolCallDisplay(
            summary=f"Browser: {action} {target}",
        )

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        if not isinstance(event.result, AgentBrowserResult):
            return ToolResultDisplay(success=True, message="Browser action complete")
        if event.result.success:
            return ToolResultDisplay(
                success=True,
                message=f"✓ Browser {event.result.action} completed",
            )
        else:
            return ToolResultDisplay(
                success=False,
                message=f"✗ Browser {event.result.action} failed: {event.result.error}",
            )

    @classmethod
    def get_status_text(cls) -> str:
        return "Browser automation via agent-browser"
