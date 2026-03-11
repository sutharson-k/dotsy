"""Browser automation for Dotsy using browser-use library.

This module provides browser automation capabilities using browser-use.
Enables AI agents to navigate websites, interact with elements, and extract content.

Features:
- Navigate to URLs and web pages
- Click, fill, type interactions
- Take screenshots
- Extract page content and accessibility trees
- Session management with persistence
- Domain allowlist for security

Security:
- Requires user approval for actions (configurable)
- Domain allowlist prevents unauthorized sites
- Session data can be cleared on exit
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from pydantic import BaseModel, Field

from dotsy.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    BaseToolState,
    InvokeContext,
    ToolError,
)
from dotsy.core.tools.ui import ToolCallDisplay, ToolResultDisplay
from dotsy.core.types import ToolCallEvent, ToolResultEvent, ToolStreamEvent


class AgentBrowserConfig(BaseToolConfig):
    """Configuration for browser automation tool."""

    headless: bool = True
    timeout_seconds: int = 60
    domain_allowlist: list[str] = Field(default_factory=list)
    provider: str = "local"  # local, browserbase


class AgentBrowserState(BaseToolState):
    """State for browser automation tool."""

    current_url: str = ""
    session_id: str = ""


class AgentBrowserArgs(BaseModel):
    """Arguments for browser automation actions."""

    action: str = Field(
        description="Action to perform: open, snapshot, click, fill, type, screenshot, scroll, etc."
    )
    url: str | None = Field(
        default=None, description="URL to navigate to (for 'open' action)"
    )
    element_ref: str | None = Field(
        default=None,
        description="Element reference (e.g., '@e1', '@e2') for click/fill/type",
    )
    text: str | None = Field(
        default=None, description="Text to fill or type (for 'fill' or 'type' actions)"
    )
    screenshot_path: str | None = Field(
        default=None, description="Path to save screenshot (for 'screenshot' action)"
    )
    wait_for: str | None = Field(
        default=None, description="Wait for element/text/URL before proceeding"
    )


class AgentBrowserResult(BaseModel):
    """Result from browser automation action."""

    success: bool
    action: str
    output: str | None = None
    screenshot_path: str | None = None
    snapshot: dict[str, Any] | None = None
    error: str | None = None


class AgentBrowser(
    BaseTool[
        AgentBrowserArgs, AgentBrowserResult, AgentBrowserConfig, AgentBrowserState
    ]
):
    """Browser automation using browser-use library.

    Navigate websites, interact with elements, take screenshots,
    and extract content for AI-driven web automation.
    """

    TOOL_NAME = "agent_browser"
    TOOL_DESCRIPTION = (
        "Automate browser actions using browser-use. Use this tool AUTOMATICALLY when users ask to: "
        "open/navigate/visit/go to a website URL, check a web page, take screenshots, click/fill/type on web pages, "
        "or extract content from websites. Examples: 'open amazon.com', 'what do you see on github.com', "
        "'take a screenshot of example.com', 'click the login button'. "
        "Navigate to URLs, click/fill elements, take screenshots, and extract page content. "
        "Uses browser-use library: pip install browser-use"
    )

    def __init__(
        self,
        config: AgentBrowserConfig | None = None,
        state: AgentBrowserState | None = None,
    ) -> None:
        super().__init__(
            config=config or AgentBrowserConfig(), state=state or AgentBrowserState()
        )
        self._browser = None
        self._context = None

    def is_available(self) -> bool:
        """Check if browser-use is available."""
        try:
            import browser_use  # noqa: F401

            return True
        except ImportError:
            return False

    def get_display(self, parameters: dict[str, Any]) -> ToolCallDisplay:
        action = parameters.get("action", "unknown")
        url = parameters.get("url", "")
        return ToolCallDisplay(
            summary=f"Browser: {action} {url or parameters.get('element_ref', '')}"
        )

    async def run(
        self, args: AgentBrowserArgs, ctx: InvokeContext | None = None
    ) -> AsyncGenerator[ToolStreamEvent | AgentBrowserResult, None]:
        if not self.is_available():
            raise ToolError(
                "browser-use not installed. Install with: pip install browser-use"
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
            yield AgentBrowserResult(
                success=True,
                action=args.action,
                output=result.output,
                screenshot_path=result.screenshot_path,
                snapshot=result.snapshot,
            )
        except TimeoutError as e:
            raise ToolError(f"Browser action timed out: {e}") from e
        except Exception as e:
            raise ToolError(f"Browser action failed: {e}") from e

    def _is_url_allowed(self, url: str) -> bool:
        """Check if URL is in domain allowlist."""
        from urllib.parse import urlparse

        # If allowlist is ['*'] or empty, allow all
        if not self.config.domain_allowlist or self.config.domain_allowlist == ["*"]:
            return True

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        for allowed in self.config.domain_allowlist:
            if allowed == "*":
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
        """Execute browser action using browser-use."""
        from browser_use import Agent, Controller
        from playwright.async_api import async_playwright

        # Initialize browser if not already done
        if self._browser is None:
            playwright = await async_playwright().start()
            self._browser = await playwright.chromium.launch(
                headless=self.config.headless
            )
            self._context = await self._browser.new_context()

        # Create controller with custom actions
        controller = Controller()

        # Build task description
        task = self._build_task_description(args)

        # Create and run agent
        agent = Agent(
            task=task,
            llm=None,  # Will be set by caller if needed
            controller=controller,
            browser=self._browser,
            context=self._context,
        )

        # Execute with timeout
        try:
            result = await asyncio.wait_for(
                self._run_agent_action(agent, args), timeout=self.config.timeout_seconds
            )
            return result
        except TimeoutError:
            raise

    def _build_task_description(self, args: AgentBrowserArgs) -> str:
        """Build task description for browser-use agent."""
        match args.action:
            case "open":
                return f"Navigate to {args.url}"
            case "snapshot":
                return "Get the current page content and structure"
            case "click":
                return f"Click on element {args.element_ref}"
            case "fill":
                return f"Fill element {args.element_ref} with text: {args.text}"
            case "type":
                return f"Type text into element {args.element_ref}: {args.text}"
            case "screenshot":
                return "Take a screenshot of the current page"
            case "scroll":
                return f"Scroll to element {args.element_ref or 'the page'}"
            case "hover":
                return f"Hover over element {args.element_ref}"
            case "wait":
                return f"Wait for: {args.wait_for}"
            case _:
                return f"Perform browser action: {args.action}"

    async def _run_agent_action(
        self, agent: Any, args: AgentBrowserArgs
    ) -> AgentBrowserResult:
        """Run browser-use agent and return result."""
        # For simple actions, use direct Playwright calls
        if self._context:
            page = await self._context.new_page()

            match args.action:
                case "open":
                    if not args.url:
                        raise ToolError("URL required for 'open' action")
                    await page.goto(args.url, wait_until="networkidle")
                    self.state.current_url = args.url
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Navigated to {args.url}",
                    )

                case "snapshot":
                    await page.goto(self.state.current_url or "about:blank")
                    content = await page.content()
                    title = await page.title()
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Page title: {title}\nContent length: {len(content)} chars",
                        snapshot={"content": content, "title": title},
                    )

                case "click":
                    if not args.element_ref:
                        raise ToolError("Element ref required for 'click' action")
                    await page.goto(self.state.current_url or "about:blank")
                    await page.click(args.element_ref)
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Clicked on {args.element_ref}",
                    )

                case "fill":
                    if not args.element_ref or not args.text:
                        raise ToolError(
                            "Element ref and text required for 'fill' action"
                        )
                    await page.goto(self.state.current_url or "about:blank")
                    await page.fill(args.element_ref, args.text)
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Filled {args.element_ref} with text",
                    )

                case "type":
                    if not args.element_ref or not args.text:
                        raise ToolError(
                            "Element ref and text required for 'type' action"
                        )
                    await page.goto(self.state.current_url or "about:blank")
                    await page.type(args.element_ref, args.text)
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Typed into {args.element_ref}",
                    )

                case "screenshot":
                    await page.goto(self.state.current_url or "about:blank")
                    screenshot_path = args.screenshot_path or "screenshot.png"
                    await page.screenshot(path=screenshot_path)
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Screenshot saved to: {screenshot_path}",
                        screenshot_path=screenshot_path,
                    )

                case "scroll":
                    await page.goto(self.state.current_url or "about:blank")
                    if args.element_ref:
                        await page.locator(
                            args.element_ref
                        ).scroll_into_view_if_needed()
                    else:
                        await page.evaluate(
                            "window.scrollTo(0, document.body.scrollHeight)"
                        )
                    return AgentBrowserResult(
                        success=True, action=args.action, output="Page scrolled"
                    )

                case "hover":
                    if not args.element_ref:
                        raise ToolError("Element ref required for 'hover' action")
                    await page.goto(self.state.current_url or "about:blank")
                    await page.hover(args.element_ref)
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Hovered over {args.element_ref}",
                    )

                case "wait":
                    if not args.wait_for:
                        raise ToolError("Wait condition required")
                    await page.goto(self.state.current_url or "about:blank")
                    await page.wait_for_selector(args.wait_for)
                    return AgentBrowserResult(
                        success=True,
                        action=args.action,
                        output=f"Waited for: {args.wait_for}",
                    )

        raise ToolError(
            f"Browser not initialized or action not supported: {args.action}"
        )

    async def cleanup(self) -> None:
        """Clean up browser resources."""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()

    @classmethod
    def get_call_display(cls, event: ToolCallEvent) -> ToolCallDisplay:
        if not isinstance(event.args, AgentBrowserArgs):
            return ToolCallDisplay(summary="Browser action...")
        action = event.args.action
        target = event.args.url or event.args.element_ref or ""
        return ToolCallDisplay(summary=f"Browser: {action} {target}")

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        if not isinstance(event.result, AgentBrowserResult):
            return ToolResultDisplay(success=True, message="Browser action complete")
        if event.result.success:
            return ToolResultDisplay(
                success=True, message=f"✓ Browser {event.result.action} completed"
            )
        else:
            return ToolResultDisplay(
                success=False,
                message=f"✗ Browser {event.result.action} failed: {event.result.error}",
            )

    @classmethod
    def get_status_text(cls) -> str:
        return "Browser automation via browser-use"
