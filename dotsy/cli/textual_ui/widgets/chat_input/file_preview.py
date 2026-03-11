from __future__ import annotations

from collections.abc import Callable
from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

from dotsy.core.attachments.handler import FileAttachment

# Constants for magic numbers
KB: int = 1024
MB: int = 1024 * 1024


class FileAttachmentPreview(Static):
    """Widget to display a preview of attached files."""

    DEFAULT_CSS = """
    FileAttachmentPreview {
        height: auto;
        max-height: 4;
        padding: 0 1;
        background: $surface;
        border: solid $primary-background;
        margin: 0 0 1 0;
    }

    FileAttachmentPreview .file-name {
        color: $text;
        text-style: bold;
    }

    FileAttachmentPreview .file-info {
        color: $text-muted;
    }

    FileAttachmentPreview .file-icon {
        width: 3;
        content-align: center middle;
    }

    FileAttachmentPreview .file-list {
        height: auto;
    }

    FileAttachmentPreview .file-item {
        height: 1;
        padding: 0 1;
    }

    FileAttachmentPreview .file-item:hover {
        background: $primary;
        color: $text;
    }

    FileAttachmentPreview .remove-btn {
        width: 3;
        content-align: center middle;
        color: $error;
        text-style: bold;
    }

    FileAttachmentPreview .remove-btn:hover {
        background: $error;
        color: $text;
    }
    """

    def __init__(
        self,
        attachments: list[FileAttachment] | None = None,
        on_remove: Callable[..., Any] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._attachments = attachments or []
        self._on_remove = on_remove

    def compose(self) -> ComposeResult:
        if not self._attachments:
            self.display = False
            return
        self.display = True
        with Vertical(classes="file-list"):
            for idx, attachment in enumerate(self._attachments):
                yield self._render_file_item(idx, attachment)

    def _render_file_item(self, idx: int, attachment: FileAttachment) -> None:
        with Horizontal(classes="file-item"):
            icon = self._get_file_icon(attachment.type)
            yield Static(icon, classes="file-icon")
            info = (
                f"{attachment.file_name} ({self._format_size(attachment.size_bytes)})"
            )
            yield Static(info, classes="file-name")
            remove_btn = Button("×", classes="remove-btn", id=f"remove-{idx}")
            yield remove_btn

    def _get_file_icon(self, file_type: str) -> str:
        icons = {"image": "🖼️", "pdf": "📄", "text": "📝", "file": "📎"}
        return icons.get(file_type, "📎")

    def _format_size(self, size_bytes: int) -> str:
        if size_bytes < KB:
            return f"{size_bytes}B"
        elif size_bytes < MB:
            return f"{size_bytes / KB:.1f}KB"
        else:
            return f"{size_bytes / MB:.1f}MB"

    def set_attachments(self, attachments: list[FileAttachment]) -> None:
        """Update the displayed attachments."""
        self._attachments = attachments
        self.refresh()
        if self._attachments:
            self.display = True
        else:
            self.display = False

    def add_attachment(self, attachment: FileAttachment) -> None:
        """Add a single attachment."""
        self._attachments.append(attachment)
        self.refresh()
        self.display = True

    def remove_attachment(self, index: int) -> None:
        """Remove an attachment by index."""
        if 0 <= index < len(self._attachments):
            self._attachments.pop(index)
            self.refresh()
            if not self._attachments:
                self.display = False
            if self._on_remove:
                self._on_remove(index)

    def get_attachments(self) -> list[FileAttachment]:
        """Get the current list of attachments."""
        return self._attachments.copy()

    def clear_attachments(self) -> None:
        """Clear all attachments."""
        self._attachments.clear()
        self.display = False
        self.refresh()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle remove button clicks."""
        if event.button.has_class("remove-btn"):
            idx = int(event.button.id.split("-")[1])
            self.remove_attachment(idx)
