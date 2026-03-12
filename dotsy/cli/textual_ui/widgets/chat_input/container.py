from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message

from dotsy.cli.autocompletion.path_completion import PathCompletionController
from dotsy.cli.autocompletion.slash_command import SlashCommandController
from dotsy.cli.commands import CommandRegistry
from dotsy.cli.textual_ui.widgets.chat_input.body import ChatInputBody
from dotsy.cli.textual_ui.widgets.chat_input.completion_manager import (
    MultiCompletionManager,
)
from dotsy.cli.textual_ui.widgets.chat_input.completion_popup import CompletionPopup
from dotsy.cli.textual_ui.widgets.chat_input.drag_drop import DragDropHandler
from dotsy.cli.textual_ui.widgets.chat_input.file_preview import FileAttachmentPreview
from dotsy.cli.textual_ui.widgets.chat_input.text_area import ChatTextArea
from dotsy.cli.textual_ui.widgets.model_selector import ModelSelectorPopup
from dotsy.core.agents import AgentSafety
from dotsy.core.attachments.handler import FileAttachment
from dotsy.core.autocompletion.completers import CommandCompleter, PathCompleter

SAFETY_BORDER_CLASSES: dict[AgentSafety, str] = {
    AgentSafety.SAFE: "border-safe",
    AgentSafety.DESTRUCTIVE: "border-warning",
    AgentSafety.YOLO: "border-error",
}


class ChatInputContainer(Vertical):
    ID_INPUT_BOX = "input-box"

    class Submitted(Message):
        def __init__(
            self, value: str, attachments: list[FileAttachment] | None = None
        ) -> None:
            self.value = value
            self.attachments = attachments or []
            super().__init__()

    def __init__(
        self,
        history_file: Path | None = None,
        command_registry: CommandRegistry | None = None,
        safety: AgentSafety = AgentSafety.NEUTRAL,
        skill_entries_getter: Callable[[], list[tuple[str, str]]] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._history_file = history_file
        self._command_registry = command_registry or CommandRegistry()
        self._safety = safety
        self._skill_entries_getter = skill_entries_getter

        # Command completer (excludes skills)
        self._command_completer = SlashCommandController(
            CommandCompleter(self._get_slash_entries), self
        )
        # Skill completer (only for /claude-* commands)
        self._skill_completer = SlashCommandController(
            CommandCompleter(self._get_skill_entries), self
        )
        self._skill_completer._is_skill_completer = True
        self._completion_manager = MultiCompletionManager([
            self._command_completer,
            self._skill_completer,
            PathCompletionController(PathCompleter(), self),
        ])
        self._completion_popup: CompletionPopup | None = None
        self._model_selector: ModelSelectorPopup | None = None
        self._body: ChatInputBody | None = None
        self._file_preview: FileAttachmentPreview | None = None
        self._drag_drop_handler: DragDropHandler | None = None
        self._attachments: list[FileAttachment] = []

    def _get_slash_entries(self) -> list[tuple[str, str]]:
        """Get command entries (excluding skills - they have separate completer)."""
        entries = [
            (alias, command.description)
            for command in self._command_registry.commands.values()
            for alias in sorted(command.aliases)
        ]
        return sorted(entries)

    def _get_skill_entries(self) -> list[tuple[str, str]]:
        """Get skill entries for separate skill completer."""
        if not self._skill_entries_getter:
            return []
        return self._skill_entries_getter()

    def compose(self) -> ComposeResult:
        self._completion_popup = CompletionPopup()
        self._model_selector = ModelSelectorPopup()
        yield self._completion_popup
        yield self._model_selector

        border_class = SAFETY_BORDER_CLASSES.get(self._safety, "")
        with Vertical(id=self.ID_INPUT_BOX, classes=border_class):
            # File attachment preview area
            self._file_preview = FileAttachmentPreview(
                on_remove=self._on_attachment_removed
            )
            yield self._file_preview

            self._body = ChatInputBody(history_file=self._history_file, id="input-body")
            yield self._body

    def on_mount(self) -> None:
        if not self._body:
            return

        self._body.set_completion_reset_callback(self._completion_manager.reset)
        if self._body.input_widget:
            self._body.input_widget.set_completion_manager(self._completion_manager)
            # Set up drag-drop handler on the text area
            self._drag_drop_handler = DragDropHandler(self)
            self._body.input_widget.register_drag_drop_handler(self._drag_drop_handler)
            self._body.focus_input()

    @property
    def input_widget(self) -> ChatTextArea | None:
        return self._body.input_widget if self._body else None

    @property
    def value(self) -> str:
        if not self._body:
            return ""
        return self._body.value

    @value.setter
    def value(self, text: str) -> None:
        if not self._body:
            return
        self._body.value = text
        widget = self._body.input_widget
        if widget:
            self._completion_manager.on_text_changed(
                widget.get_full_text(), widget._get_full_cursor_offset()
            )

    def focus_input(self) -> None:
        if self._body:
            self._body.focus_input()

    def render_completion_suggestions(
        self, suggestions: list[tuple[str, str]], selected_index: int
    ) -> None:
        if self._completion_popup:
            self._completion_popup.update_suggestions(suggestions, selected_index)

    def clear_completion_suggestions(self) -> None:
        if self._completion_popup:
            self._completion_popup.hide()

    def show_model_selector(
        self, models: list[dict], current_model: str | None = None
    ) -> None:
        """Show the model selector popup."""
        if self._model_selector:
            self._model_selector.set_models(models, current_model)
        if self._completion_popup:
            self._completion_popup.hide()

    def hide_model_selector(self) -> None:
        """Hide the model selector popup."""
        if self._model_selector:
            self._model_selector.hide()

    def navigate_model_selector(self, direction: int) -> None:
        """Navigate model selector with arrow keys."""
        if self._model_selector and self._model_selector.styles.display != "none":
            self._model_selector.navigate(direction)

    def add_model_search(self, char: str) -> None:
        """Add character to model search."""
        if self._model_selector:
            self._model_selector.add_search_char(char)

    def clear_model_search(self) -> None:
        """Clear model search."""
        if self._model_selector:
            self._model_selector.clear_search()

    @property
    def selected_model(self) -> str | None:
        """Get the currently selected model."""
        if self._model_selector:
            return self._model_selector.selected_model
        return None

    def _format_insertion(self, replacement: str, suffix: str) -> str:
        """Format the insertion text with appropriate spacing."""
        if replacement.startswith("@"):
            if replacement.endswith("/"):
                return replacement
            return replacement + (" " if not suffix or not suffix[0].isspace() else "")
        return replacement + (" " if suffix and not suffix[0].isspace() else "")

    def replace_completion_range(self, start: int, end: int, replacement: str) -> None:
        widget = self.input_widget
        if not widget or not self._body:
            return
        start, end, replacement = widget.adjust_from_full_text_coords(
            start, end, replacement
        )

        text = widget.text
        start = max(0, min(start, len(text)))
        end = max(start, min(end, len(text)))

        prefix = text[:start]
        suffix = text[end:]
        insertion = self._format_insertion(replacement, suffix)
        new_text = f"{prefix}{insertion}{suffix}"

        self._body.replace_input(new_text, cursor_offset=start + len(insertion))

    def on_chat_input_body_submitted(self, event: ChatInputBody.Submitted) -> None:
        event.stop()
        self.post_message(self.Submitted(event.value, self._attachments.copy()))
        # Clear attachments after submission
        self._attachments.clear()
        if self._file_preview:
            self._file_preview.clear_attachments()

    def set_safety(self, safety: AgentSafety) -> None:
        self._safety = safety

        try:
            input_box = self.get_widget_by_id(self.ID_INPUT_BOX)
        except Exception:
            return

        for border_class in SAFETY_BORDER_CLASSES.values():
            input_box.remove_class(border_class)

        if safety in SAFETY_BORDER_CLASSES:
            input_box.add_class(SAFETY_BORDER_CLASSES[safety])

    def on_drag_drop_handler_file_dropped(
        self, event: DragDropHandler.FileDropped
    ) -> None:
        """Handle files dropped via drag-and-drop."""
        valid_attachments, rejected_files = DragDropHandler.process_dropped_files(
            event.file_paths
        )

        if rejected_files:
            # Notify about unsupported file types
            from dotsy.cli.textual_ui.app import DotsyApp
            from dotsy.cli.textual_ui.widgets.messages import WarningMessage

            app = self.app
            if isinstance(app, DotsyApp):
                unsupported = ", ".join(Path(f).name for f in rejected_files)
                warning_msg = WarningMessage(
                    f"Unsupported file type(s): {unsupported}\n"
                    f"Supported: Images, PDFs, and text files"
                )
                app.run_worker(app._mount_and_scroll(warning_msg))

        if valid_attachments:
            self._attachments.extend(valid_attachments)
            if self._file_preview:
                for attachment in valid_attachments:
                    self._file_preview.add_attachment(attachment)

    def _on_attachment_removed(self, index: int) -> None:
        """Handle attachment removal from preview."""
        if 0 <= index < len(self._attachments):
            self._attachments.pop(index)

    def get_attachments(self) -> list[FileAttachment]:
        """Get current attachments."""
        return self._attachments.copy()

    def clear_attachments(self) -> None:
        """Clear all attachments."""
        self._attachments.clear()
        if self._file_preview:
            self._file_preview.clear_attachments()
