"""Model selector popup widget for dotsy."""

from __future__ import annotations

from rich.text import Text
from textual.widgets import Static


class ModelSelectorPopup(Static):
    """Popup widget for selecting AI models with arrow key navigation."""

    def __init__(self, **kwargs) -> None:
        super().__init__("", id="model-selector-popup", **kwargs)
        self.styles.display = "none"
        self.can_focus = False
        self._models: list[dict] = []
        self._selected_index = 0

    def set_models(self, models: list[dict]) -> None:
        """Set the list of available models.
        
        Args:
            models: List of dicts with 'alias', 'name', 'provider' keys
        """
        self._models = models
        self._selected_index = 0
        self._update_display()

    def navigate(self, direction: int) -> None:
        """Navigate through models using arrow keys.
        
        Args:
            direction: 1 for down, -1 for up
        """
        if not self._models:
            return
            
        self._selected_index = (self._selected_index + direction) % len(self._models)
        self._update_display()

    @property
    def selected_model(self) -> str | None:
        """Get the currently selected model alias."""
        if not self._models:
            return None
        return self._models[self._selected_index].get('alias')

    def _update_display(self) -> None:
        """Update the popup display with current selection."""
        if not self._models:
            self.hide()
            return

        text = Text()
        text.append("### Select Model (↑↓ to navigate, Enter to select)\n\n", style="bold")
        
        for idx, model in enumerate(self._models):
            if idx:
                text.append("\n")

            alias = model.get('alias', 'unknown')
            name = model.get('name', '')
            provider = model.get('provider', '')
            
            if idx == self._selected_index:
                # Selected item with reverse video
                text.append(f" ● {alias}", style="bold reverse")
                text.append(f"  ({name} - {provider})", style="italic reverse")
            else:
                # Normal item
                text.append(f"   {alias}", style="bold")
                text.append(f"  ({name} - {provider})", style="dim")

        self.update(text)
        self.show()

    def hide(self) -> None:
        """Hide the popup."""
        self.update("")
        self.styles.display = "none"

    def show(self) -> None:
        """Show the popup."""
        self.styles.display = "block"
