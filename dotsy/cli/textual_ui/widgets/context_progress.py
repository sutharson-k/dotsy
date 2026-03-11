from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any

from textual.reactive import reactive

from dotsy.cli.textual_ui.widgets.no_markup_static import NoMarkupStatic


@dataclass
class TokenState:
    max_tokens: int = 0
    current_tokens: int = 0


@dataclass
class TokenTracking:
    """Tracks token usage over time for rate calculation."""

    start_time: float = 0.0
    last_tokens: int = 0


class ContextProgress(NoMarkupStatic):
    tokens = reactive(TokenState())
    tracking = reactive(TokenTracking())

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def watch_tokens(self, new_state: TokenState) -> None:
        if new_state.max_tokens == 0:
            self.update("")
            return

        ratio = min(1, new_state.current_tokens / new_state.max_tokens)

        # Calculate tokens per second
        tokens_per_second = ""
        current_time = time.time()
        if self.tracking.start_time == 0.0:
            self.tracking = TokenTracking(
                start_time=current_time, last_tokens=new_state.current_tokens
            )
        else:
            elapsed = current_time - self.tracking.start_time
            tokens_added = new_state.current_tokens - self.tracking.last_tokens
            if elapsed > 0 and tokens_added > 0:
                rate = tokens_added / elapsed
                tokens_per_second = f" ({rate:.1f} tok/s)"
            # Reset tracking if tokens decreased (e.g., after compact)
            if new_state.current_tokens < self.tracking.last_tokens:
                self.tracking = TokenTracking(
                    start_time=current_time, last_tokens=new_state.current_tokens
                )
            else:
                self.tracking = TokenTracking(
                    start_time=self.tracking.start_time,
                    last_tokens=new_state.current_tokens,
                )

        text = (
            f"{ratio:.0%} of {new_state.max_tokens // 1000}k tokens{tokens_per_second}"
        )
        self.update(text)
