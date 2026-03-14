"""Model selector widget for dotsy with providers and models view."""

from __future__ import annotations

from typing import Any

from rich.text import Text
from textual.events import Click, MouseMove
from textual.widgets import Static


class ModelSelectorWidget(Static):
    """Model selector with CURRENT MODEL and PROVIDERS sections."""
    
    BINDINGS = [
        ("enter", "select", "Select"),
        ("escape", "cancel", "Cancel"),
        ("backspace", "back", "Back"),
    ]
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__("", id="model-selector", **kwargs)
        self.styles.display = "none"
        self.can_focus = True
        self._models: list[dict] = []
        self._providers: dict[str, list[dict]] = {}
        self._current_model: str | None = None
        self._selected_provider: str | None = None
        self._selected_model_index = 0
        self._mode = "providers"  # "providers" or "models"
        
    def set_models(self, models: list[dict], current_model: str | None = None) -> None:
        """Set the list of available models and group by provider.
        
        Args:
            models: List of dicts with 'alias', 'name', 'provider' keys
            current_model: The currently active model alias
        """
        self._models = models
        self._current_model = current_model
        self._group_by_provider()
        self._selected_model_index = 0
        # Auto-select first provider
        provider_list = sorted(self._providers.keys())
        self._selected_provider = provider_list[0] if provider_list else None
        self._mode = "providers"
        self._update_display()
        
    def _group_by_provider(self) -> None:
        """Group models by provider."""
        self._providers = {}
        for model in self._models:
            provider = model.get("provider", "unknown")
            if provider not in self._providers:
                self._providers[provider] = []
            self._providers[provider].append(model)
            
    def navigate(self, direction: int) -> None:
        """Navigate using arrow keys.
        
        Args:
            direction: 1 for down, -1 for up
        """
        if self._mode == "providers":
            self._navigate_providers(direction)
        else:
            self._navigate_models(direction)
            
    def _navigate_providers(self, direction: int) -> None:
        """Navigate through providers list."""
        provider_list = sorted(self._providers.keys())
        if not provider_list:
            return

        if self._selected_provider is None:
            self._selected_provider = provider_list[0]
        else:
            idx = provider_list.index(self._selected_provider)
            idx = (idx + direction) % len(provider_list)
            self._selected_provider = provider_list[idx]
        self._update_display()
        
    def _navigate_models(self, direction: int) -> None:
        """Navigate through models list."""
        if not self._selected_provider:
            return
        models = sorted(self._providers.get(self._selected_provider, []), key=lambda m: m.get("alias", ""))
        if not models:
            return
        self._selected_model_index = (self._selected_model_index + direction) % len(models)
        self._update_display()
        
    def select(self) -> str | None:
        """Select current item (Enter key).
        
        Returns:
            Selected model alias or None
        """
        if self._mode == "providers":
            if self._selected_provider:
                self._mode = "models"
                self._selected_model_index = 0
                self._update_display()
        else:
            if self._selected_provider:
                models = sorted(self._providers.get(self._selected_provider, []), key=lambda m: m.get("alias", ""))
                if models and 0 <= self._selected_model_index < len(models):
                    return models[self._selected_model_index].get("alias")
        return None
        
    def back(self) -> None:
        """Go back to providers list."""
        self._mode = "providers"
        self._selected_model_index = 0
        self._selected_provider = sorted(self._providers.keys())[0] if self._providers else None
        self._update_display()
        
    @property
    def selected_model(self) -> str | None:
        """Get the currently selected model alias."""
        if self._selected_provider and self._mode == "models":
            models = sorted(self._providers.get(self._selected_provider, []), key=lambda m: m.get("alias", ""))
            if models and 0 <= self._selected_model_index < len(models):
                return models[self._selected_model_index].get("alias")
        return None
        
    def _update_display(self) -> None:
        """Update the display with current selection."""
        text = Text()
        
        # Header
        text.append("╔══════════════════════════════════════════════════════════╗\n", style="bold cyan")
        if self._mode == "providers":
            text.append("║         MODEL SELECTOR - Select a Provider            ║\n", style="bold cyan")
        else:
            text.append("║         MODEL SELECTOR - Select a Model               ║\n", style="bold cyan")
        text.append("╚══════════════════════════════════════════════════════════╝\n\n", style="bold cyan")
        
        # Current Model Section
        text.append("┌──────────────────────────────────────────────────────────┐\n", style="bold green")
        text.append("│ ", style="bold green")
        text.append("CURRENT MODEL", style="bold reverse green")
        text.append(" " * 46, style="bold green")
        text.append("│\n", style="bold green")
        text.append("│ ", style="green")
        if self._current_model:
            text.append(f"● {self._current_model}", style="bold yellow")
            text.append(" " * (53 - len(self._current_model)), style="green")
        else:
            text.append("No model selected", style="dim yellow")
            text.append(" " * 34, style="green")
        text.append("│\n", style="green")
        text.append("└──────────────────────────────────────────────────────────┘\n\n", style="bold green")
        
        # Providers Section
        text.append("┌──────────────────────────────────────────────────────────┐\n", style="bold cyan")
        text.append("│ ", style="bold cyan")
        if self._mode == "providers":
            text.append("PROVIDERS (select to view models)", style="bold reverse cyan")
        else:
            text.append(f"PROVIDERS → {self._selected_provider}", style="bold reverse cyan")
        text.append(" " * (14 if self._mode == "providers" else max(0, 14 - len(str(self._selected_provider)))), style="bold cyan")
        text.append("│\n", style="bold cyan")
        text.append("│                                                          │\n", style="cyan")
        
        if self._mode == "providers":
            # Show all providers
            provider_list = sorted(self._providers.keys())
            for idx, provider in enumerate(provider_list):
                model_count = len(self._providers[provider])
                is_selected = provider == self._selected_provider
                is_current_provider = self._current_model and any(
                    m.get("alias") == self._current_model for m in self._providers[provider]
                )
                
                if is_selected:
                    text.append("│  ", style="cyan")
                    text.append(f"▶ {provider}", style="bold reverse")
                    text.append(" " * (35 - len(provider)), style="reverse")
                    text.append(f" {model_count} models", style="reverse dim")
                    text.append("  │\n", style="reverse")
                else:
                    marker = "✓" if is_current_provider else " "
                    text.append(f"│  {marker} {provider}", style="cyan")
                    text.append(" " * (35 - len(provider)), style="dim")
                    text.append(f" {model_count} models  │\n", style="dim")
        else:
            # Show models for selected provider
            models = sorted(self._providers.get(self._selected_provider, []), key=lambda m: m.get("alias", ""))
            for idx, model in enumerate(models):
                alias = model.get("alias", "unknown")
                name = model.get("name", "")
                is_selected = idx == self._selected_model_index
                is_current = alias == self._current_model
                
                if is_selected:
                    text.append("│  ", style="cyan")
                    if is_current:
                        text.append(f"▶ {alias} ✓", style="bold reverse yellow")
                        text.append(" " * (35 - len(alias)), style="reverse yellow")
                    else:
                        text.append(f"▶ {alias}", style="bold reverse")
                        text.append(" " * (37 - len(alias)), style="reverse")
                    text.append("  │\n", style="reverse")
                else:
                    marker = "●" if is_current else " "
                    text.append(f"│  {marker} {alias}", style="cyan")
                    text.append(" " * (37 - len(alias)), style="dim")
                    text.append("  │\n", style="dim")
                    
            # Back option
            text.append("│                                                          │\n", style="cyan")
            text.append("│  ", style="cyan")
            text.append("← Back to Providers", style="italic yellow")
            text.append(" " * 30, style="dim")
            text.append("│\n", style="cyan")
            
        text.append("│                                                          │\n", style="cyan")
        text.append("└──────────────────────────────────────────────────────────┘\n", style="bold cyan")
        
        # Help footer
        text.append("\n", style="dim")
        text.append("  ↑↓: Navigate  Enter: Select  Backspace: Back  Esc: Cancel", style="dim italic")
        
        self.update(text)
        self.refresh()

    def action_select(self) -> None:
        """Handle Enter key."""
        alias = self.select()
        if alias:
            self.hide()
            from dotsy.core.config import DotsyConfig
            DotsyConfig.save_updates({"active_model": alias})
            import asyncio
            asyncio.create_task(self.app._reload_config())
            # Refocus chat input
            try:
                self.app.query_one("ChatInputContainer").focus_input()
            except Exception:
                pass

    def action_cancel(self) -> None:
        """Handle Escape key."""
        self.hide()
        # Refocus chat input
        try:
            self.app.query_one("ChatInputContainer").focus_input()
        except Exception:
            pass
        
    def action_back(self) -> None:
        """Handle Backspace key."""
        self.back()
        
    def hide(self) -> None:
        """Hide the model selector."""
        self.styles.display = "none"
        self.can_focus = False
        
    def show(self) -> None:
        """Show the model selector."""
        self.styles.display = "block"
        self.can_focus = True
        
    def on_click(self, event: Click) -> None:
        """Handle click events for selecting providers/models."""
        if self._mode == "providers":
            if self._selected_provider:
                self._mode = "models"
                self._selected_model_index = 0
                self.focus()
                self._update_display()
        else:
            alias = self.selected_model
            if alias:
                self.hide()
                from dotsy.core.config import DotsyConfig
                DotsyConfig.save_updates({"active_model": alias})
                import asyncio
                asyncio.create_task(self.app._reload_config())
                try:
                    self.app.query_one("ChatInputContainer").focus_input()
                except Exception:
                    pass

    def on_mouse_move(self, event: MouseMove) -> None:
        """Handle mouse hover to highlight providers/models."""
        y = event.offset.y
        if self._mode == "providers":
            provider_list = sorted(self._providers.keys())
            idx = y - 14
            if 0 <= idx < len(provider_list):
                self._selected_provider = provider_list[idx]
                self._update_display()
        else:
            models = sorted(self._providers.get(self._selected_provider, []), key=lambda m: m.get("alias", ""))
            idx = y - 14
            if 0 <= idx < len(models):
                self._selected_model_index = idx
                self._update_display()

