"""Model selector popup widget for dotsy."""

from __future__ import annotations

from typing import Any

from rich.text import Text
from textual.widgets import Static


class ModelSelectorPopup(Static):
    """Popup widget for selecting AI models with arrow key navigation and search."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__("", id="model-selector-popup", **kwargs)
        self.styles.display = "none"
        self.can_focus = False
        self._models: list[dict] = []
        self._filtered_models: list[dict] = []
        self._selected_index = 0
        self._search_term = ""

    def set_models(self, models: list[dict], current_model: str | None = None) -> None:
        """Set the list of available models.

        Args:
            models: List of dicts with 'alias', 'name', 'provider' keys
            current_model: The currently active model alias
        """
        self._models = models
        self._current_model = current_model
        self._search_term = ""
        self._selected_index = 0
        # Start selection at current model if found
        if current_model:
            for idx, model in enumerate(models):
                if model.get("alias") == current_model:
                    self._selected_index = idx
                    break
        self._apply_filter()

    def _apply_filter(self) -> None:
        """Apply search filter to models list."""
        if not self._search_term:
            self._filtered_models = self._models
        else:
            search_lower = self._search_term.lower()
            self._filtered_models = [
                m
                for m in self._models
                if (
                    search_lower in m.get("alias", "").lower()
                    or search_lower in m.get("name", "").lower()
                    or search_lower in m.get("provider", "").lower()
                )
            ]
        # Reset selection to first match or current model
        self._selected_index = 0
        if self._current_model and self._filtered_models:
            for idx, model in enumerate(self._filtered_models):
                if model.get("alias") == self._current_model:
                    self._selected_index = idx
                    break
        self._update_display()

    def add_search_char(self, char: str) -> None:
        """Add character to search term."""
        self._search_term += char
        self._selected_index = 0
        self._apply_filter()

    def clear_search(self) -> None:
        """Clear search term."""
        self._search_term = ""
        self._selected_index = 0
        self._filtered_models = self._models.copy()
        # Find current model in the list
        if self._current_model:
            for idx, model in enumerate(self._filtered_models):
                if model.get("alias") == self._current_model:
                    self._selected_index = idx
                    break
        self._update_display()

    def navigate(self, direction: int) -> None:
        """Navigate through models using arrow keys.

        Args:
            direction: 1 for down, -1 for up
        """
        if not self._filtered_models:
            return

        self._selected_index = (self._selected_index + direction) % len(
            self._filtered_models
        )
        self._update_display()

    @property
    def selected_model(self) -> str | None:
        """Get the currently selected model alias."""
        if not self._models:
            return None
        return self._models[self._selected_index].get("alias")

    def _update_display(self) -> None:
        """Update the popup display with current selection."""
        # Don't hide if searching - show "no results" message instead
        if not self._filtered_models and not self._search_term:
            self.hide()
            return

        text = Text()
        search_hint = " (type to search)" if not self._search_term else ""
        text.append(
            f"### Select Model (↑↓ navigate, Enter select{search_hint})\n\n",
            style="bold",
        )

        if self._search_term:
            text.append(
                f'Search: "{self._search_term}" ({len(self._filtered_models)}/{len(self._models)} models)\n\n',
                style="italic cyan",
            )

        if not self._filtered_models:
            text.append("  No models match your search.\n", style="dim yellow")
            text.append("  Press Escape to clear search.\n", style="dim yellow")
            self.update(text)
            self.refresh()  # Force immediate re-render
            self.show()
            return

        for idx, model in enumerate(self._filtered_models):
            if idx:
                text.append("\n")

            alias = model.get("alias", "unknown")
            name = model.get("name", "")
            provider = model.get("provider", "")
            is_current = self._current_model and alias == self._current_model

            if idx == self._selected_index:
                # Selected item with reverse video
                if is_current:
                    text.append(f" ● {alias} ✓", style="bold reverse green")
                    text.append(
                        f"  ({name} - {provider}) [CURRENT]",
                        style="italic reverse green",
                    )
                else:
                    text.append(f" ● {alias}", style="bold reverse")
                    text.append(f"  ({name} - {provider})", style="italic reverse")
            # Normal item
            elif is_current:
                text.append(f"   {alias} ✓", style="bold green")
                text.append(f"  ({name} - {provider}) [CURRENT]", style="dim green")
            else:
                text.append(f"   {alias}", style="bold")
                text.append(f"  ({name} - {provider})", style="dim")

        self.update(text)
        self.refresh()  # Force immediate re-render
        self.show()

    def hide(self) -> None:
        """Hide the popup."""
        self.update("")
        self.styles.display = "none"

    def show(self) -> None:
        """Show the popup."""
        self.styles.display = "block"
