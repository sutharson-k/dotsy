"""Computer control tool for Dotsy.

Provides full system control: screenshots, mouse, keyboard, window management.
Allows the AI to see and interact with any application on the desktop.

Requirements (auto-installed if missing):
    pip install pyautogui pillow pygetwindow pynput
"""

from __future__ import annotations

import asyncio
import base64
import io
import platform
import time
from collections.abc import AsyncGenerator
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from dotsy.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    BaseToolState,
    InvokeContext,
    ToolError,
)
from dotsy.core.tools.ui import ToolCallDisplay, ToolResultDisplay, ToolUIData
from dotsy.core.types import ToolCallEvent, ToolResultEvent, ToolStreamEvent


def _check_deps() -> None:
    """Check and provide helpful error if deps missing."""
    try:
        import pyautogui  # noqa: F401
    except ImportError:
        raise ToolError(
            "pyautogui is not installed. Run: pip install pyautogui pillow"
        )


def _get_pyautogui():
    """Lazy import pyautogui."""
    try:
        import pyautogui
        pyautogui.FAILSAFE = True  # move mouse to corner to abort
        pyautogui.PAUSE = 0.1
        return pyautogui
    except ImportError:
        raise ToolError("pyautogui not installed. Run: pip install pyautogui pillow")


def _get_pil():
    """Lazy import PIL."""
    try:
        from PIL import Image
        return Image
    except ImportError:
        raise ToolError("Pillow not installed. Run: pip install pillow")


def _take_screenshot(region: tuple[int, int, int, int] | None = None) -> str:
    """Take screenshot and return as base64 PNG."""
    pyautogui = _get_pyautogui()
    Image = _get_pil()

    screenshot = pyautogui.screenshot(region=region)

    # Resize to max 1280px wide to save tokens
    max_width = 1280
    if screenshot.width > max_width:
        ratio = max_width / screenshot.width
        new_size = (max_width, int(screenshot.height * ratio))
        screenshot = screenshot.resize(new_size, Image.LANCZOS)

    buf = io.BytesIO()
    screenshot.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _list_windows() -> list[dict[str, str]]:
    """List all open windows."""
    try:
        import pygetwindow as gw
        windows = gw.getAllWindows()
        return [
            {"title": w.title, "visible": str(w.visible), "active": str(w.isActive)}
            for w in windows
            if w.title.strip()
        ]
    except ImportError:
        # Fallback: use wmctrl on Linux
        try:
            import subprocess
            result = subprocess.run(
                ["wmctrl", "-l"], capture_output=True, text=True, timeout=3
            )
            lines = result.stdout.strip().splitlines()
            return [{"title": " ".join(l.split()[3:]), "visible": "true"} for l in lines if l]
        except Exception:
            return [{"title": "pygetwindow not installed — run: pip install pygetwindow", "visible": "false"}]


def _focus_window(title: str) -> str:
    """Focus a window by title (partial match)."""
    try:
        import pygetwindow as gw
        matches = gw.getWindowsWithTitle(title)
        if not matches:
            return f"No window found with title containing '{title}'"
        matches[0].activate()
        time.sleep(0.3)
        return f"Focused: {matches[0].title}"
    except ImportError:
        # Linux fallback
        try:
            import subprocess
            result = subprocess.run(
                ["wmctrl", "-a", title], capture_output=True, text=True, timeout=3
            )
            return f"Attempted focus on '{title}'"
        except Exception as e:
            return f"Could not focus window: {e}"


class ComputerConfig(BaseToolConfig):
    """Configuration for computer control tool."""
    screenshot_quality: int = Field(default=80, ge=10, le=100)
    move_duration: float = Field(default=0.2, ge=0.0, le=2.0)
    type_interval: float = Field(default=0.02, ge=0.0, le=0.5)


class ComputerState(BaseToolState):
    pass


class ComputerArgs(BaseModel):
    """Arguments for computer control."""

    action: Literal[
        "screenshot",
        "click",
        "right_click",
        "double_click",
        "move",
        "drag",
        "type",
        "hotkey",
        "key",
        "scroll",
        "get_windows",
        "focus_window",
        "get_cursor_pos",
        "get_screen_size",
    ] = Field(description=(
        "Action to perform:\n"
        "- screenshot: Take a screenshot (optionally of a region)\n"
        "- click: Left click at x,y\n"
        "- right_click: Right click at x,y\n"
        "- double_click: Double click at x,y\n"
        "- move: Move mouse to x,y\n"
        "- drag: Drag from x,y to x2,y2\n"
        "- type: Type text string\n"
        "- hotkey: Press key combination (e.g. ctrl+c, alt+f4)\n"
        "- key: Press single key (e.g. enter, tab, escape, f5)\n"
        "- scroll: Scroll at x,y by clicks amount (positive=up, negative=down)\n"
        "- get_windows: List all open windows\n"
        "- focus_window: Focus a window by title\n"
        "- get_cursor_pos: Get current mouse cursor position\n"
        "- get_screen_size: Get screen resolution\n"
    ))

    x: int | None = Field(default=None, description="X coordinate for mouse actions")
    y: int | None = Field(default=None, description="Y coordinate for mouse actions")
    x2: int | None = Field(default=None, description="End X coordinate for drag")
    y2: int | None = Field(default=None, description="End Y coordinate for drag")
    text: str | None = Field(default=None, description="Text to type or key/hotkey to press")
    clicks: int | None = Field(default=None, description="Number of scroll clicks (positive=up, negative=down)")
    region: list[int] | None = Field(
        default=None,
        description="Screenshot region [x, y, width, height]. Leave empty for full screen."
    )
    window_title: str | None = Field(default=None, description="Window title for focus_window action")
    delay_seconds: float | None = Field(
        default=None,
        description="Wait this many seconds before performing the action. Use this instead of asking the user."
    )


class ComputerResult(BaseModel):
    """Result from computer control action."""
    action: str
    success: bool
    message: str
    screenshot_b64: str | None = None
    data: dict | None = None


class Computer(
    BaseTool[ComputerArgs, ComputerResult, ComputerConfig, ComputerState],
    ToolUIData[ComputerArgs, ComputerResult],
):
    """Control the entire computer: screenshots, mouse, keyboard, windows.

    Can see the screen and interact with ANY application — Blender, Unity,
    VS Code, browsers, games, or anything else running on the desktop.

    Always take a screenshot first to see the current state before acting.
    Use hotkey for keyboard shortcuts (e.g. ctrl+s to save, alt+tab to switch).
    """

    TOOL_NAME = "computer"
    TOOL_DESCRIPTION = (
        "Full system control: take screenshots to see the screen, move/click "
        "the mouse, type text, press keyboard shortcuts, and manage windows. "
        "Can interact with ANY application on the desktop. "
        "Always screenshot first to understand the current state. "
        "IMPORTANT: Never ask clarifying questions for screenshot or delay requests. "
        "If user says 'take a screenshot in 5 seconds', use delay_seconds=5 and action=screenshot immediately. "
        "If user says 'take a screenshot', just do it — default to full screen, no questions."
    )
    TOOL_PROMPT_FILE: ClassVar[str] = ""

    @classmethod
    def get_tool_prompt(cls) -> str:
        return (
            "## Computer Control Tool\n"
            "You can control the entire desktop using the `computer` tool.\n"
            "Workflow: screenshot → analyse → act → screenshot to verify.\n"
            "SAFETY: pyautogui failsafe is ON — moving mouse to top-left corner aborts.\n"
            "Always take a screenshot before and after each action to verify results.\n"
        )

    def get_call_display(self, args: ComputerArgs) -> ToolCallDisplay:
        label = f"computer: {args.action}"
        if args.action in ("click", "double_click", "right_click", "move") and args.x is not None:
            label += f" ({args.x}, {args.y})"
        elif args.action == "type" and args.text:
            label += f' "{args.text[:40]}{"..." if len(args.text) > 40 else ""}"'
        elif args.action in ("hotkey", "key") and args.text:
            label += f" [{args.text}]"
        elif args.action == "focus_window" and args.window_title:
            label += f' "{args.window_title}"'
        return ToolCallDisplay(label=label)

    def get_result_display(self, result: ComputerResult) -> ToolResultDisplay:
        icon = "✓" if result.success else "✗"
        return ToolResultDisplay(label=f"{icon} {result.message}")

    async def _execute(self, args: ComputerArgs) -> ComputerResult:
        loop = asyncio.get_event_loop()

        if args.delay_seconds and args.delay_seconds > 0:
            await asyncio.sleep(args.delay_seconds)

        if args.action == "screenshot":
            region = tuple(args.region) if args.region and len(args.region) == 4 else None
            b64 = await loop.run_in_executor(None, _take_screenshot, region)
            return ComputerResult(
                action="screenshot",
                success=True,
                message="Screenshot taken",
                screenshot_b64=b64,
            )

        elif args.action in ("click", "right_click", "double_click"):
            if args.x is None or args.y is None:
                raise ToolError("x and y required for click actions")
            pyautogui = _get_pyautogui()

            def do_click():
                if args.action == "right_click":
                    pyautogui.rightClick(args.x, args.y)
                elif args.action == "double_click":
                    pyautogui.doubleClick(args.x, args.y)
                else:
                    pyautogui.click(args.x, args.y)

            await loop.run_in_executor(None, do_click)
            return ComputerResult(
                action=args.action,
                success=True,
                message=f"{args.action} at ({args.x}, {args.y})",
            )

        elif args.action == "move":
            if args.x is None or args.y is None:
                raise ToolError("x and y required for move")
            pyautogui = _get_pyautogui()
            await loop.run_in_executor(
                None, lambda: pyautogui.moveTo(args.x, args.y, duration=0.2)
            )
            return ComputerResult(
                action="move", success=True,
                message=f"Mouse moved to ({args.x}, {args.y})"
            )

        elif args.action == "drag":
            if args.x is None or args.y is None or args.x2 is None or args.y2 is None:
                raise ToolError("x, y, x2, y2 required for drag")
            pyautogui = _get_pyautogui()
            await loop.run_in_executor(
                None,
                lambda: pyautogui.drag(args.x2 - args.x, args.y2 - args.y,
                                        duration=0.3, startX=args.x, startY=args.y)
            )
            return ComputerResult(
                action="drag", success=True,
                message=f"Dragged from ({args.x},{args.y}) to ({args.x2},{args.y2})"
            )

        elif args.action == "type":
            if not args.text:
                raise ToolError("text required for type action")
            pyautogui = _get_pyautogui()
            await loop.run_in_executor(
                None, lambda: pyautogui.typewrite(args.text, interval=0.02)
            )
            return ComputerResult(
                action="type", success=True,
                message=f"Typed: {args.text[:50]}{'...' if len(args.text) > 50 else ''}"
            )

        elif args.action == "hotkey":
            if not args.text:
                raise ToolError("text required for hotkey (e.g. 'ctrl+c')")
            pyautogui = _get_pyautogui()
            keys = [k.strip() for k in args.text.split("+")]
            await loop.run_in_executor(
                None, lambda: pyautogui.hotkey(*keys)
            )
            return ComputerResult(
                action="hotkey", success=True,
                message=f"Pressed hotkey: {args.text}"
            )

        elif args.action == "key":
            if not args.text:
                raise ToolError("text required for key (e.g. 'enter', 'tab', 'f5')")
            pyautogui = _get_pyautogui()
            await loop.run_in_executor(
                None, lambda: pyautogui.press(args.text)
            )
            return ComputerResult(
                action="key", success=True,
                message=f"Pressed key: {args.text}"
            )

        elif args.action == "scroll":
            if args.x is None or args.y is None:
                raise ToolError("x and y required for scroll")
            clicks = args.clicks or 3
            pyautogui = _get_pyautogui()
            await loop.run_in_executor(
                None, lambda: pyautogui.scroll(clicks, x=args.x, y=args.y)
            )
            direction = "up" if clicks > 0 else "down"
            return ComputerResult(
                action="scroll", success=True,
                message=f"Scrolled {direction} {abs(clicks)} clicks at ({args.x},{args.y})"
            )

        elif args.action == "get_windows":
            windows = await loop.run_in_executor(None, _list_windows)
            return ComputerResult(
                action="get_windows", success=True,
                message=f"Found {len(windows)} windows",
                data={"windows": windows}
            )

        elif args.action == "focus_window":
            title = args.window_title or args.text or ""
            if not title:
                raise ToolError("window_title required for focus_window")
            msg = await loop.run_in_executor(None, _focus_window, title)
            return ComputerResult(
                action="focus_window", success=True, message=msg
            )

        elif args.action == "get_cursor_pos":
            pyautogui = _get_pyautogui()
            pos = await loop.run_in_executor(None, pyautogui.position)
            return ComputerResult(
                action="get_cursor_pos", success=True,
                message=f"Cursor at ({pos.x}, {pos.y})",
                data={"x": pos.x, "y": pos.y}
            )

        elif args.action == "get_screen_size":
            pyautogui = _get_pyautogui()
            size = await loop.run_in_executor(None, pyautogui.size)
            return ComputerResult(
                action="get_screen_size", success=True,
                message=f"Screen: {size.width}x{size.height}",
                data={"width": size.width, "height": size.height}
            )

        else:
            raise ToolError(f"Unknown action: {args.action}")

    async def invoke(
        self, ctx: InvokeContext, **kwargs
    ) -> AsyncGenerator[ToolStreamEvent | ComputerResult]:
        args = ComputerArgs(**kwargs)

        yield ToolStreamEvent(
            tool_call_id=ctx.tool_call_id,
            content=f"executing {args.action}...",
        )

        try:
            result = await self._execute(args)
            yield result
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Computer action '{args.action}' failed: {e}") from e
