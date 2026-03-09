"""Drag-and-drop file handler for DOTSY CLI."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

from textual import events
from textual.message import Message

from dotsy.core.attachments.handler import AttachmentHandler, FileAttachment

if TYPE_CHECKING:
    from dotsy.cli.textual_ui.widgets.chat_input.container import ChatInputContainer


class DragDropHandler:
    """Handles drag-and-drop events for file attachments."""

    def __init__(self, chat_container: ChatInputContainer) -> None:
        self.chat_container = chat_container
        self.attachment_handler = AttachmentHandler()

    class FileDropped(Message):
        """Message sent when files are dropped."""

        def __init__(self, file_paths: list[str]) -> None:
            self.file_paths = file_paths
            super().__init__()

    async def on_drop(self, event: events.Drop) -> None:
        """Handle drop event."""
        event.prevent_default()
        event.stop()

        file_paths = []
        for item in event.paths:
            file_paths.append(str(item))

        if file_paths:
            self.chat_container.post_message(self.FileDropped(file_paths))

    def on_drag_enter(self, event: events.DragEnter) -> None:
        """Handle drag enter event - show drop zone highlight."""
        event.prevent_default()
        # Add visual feedback for drag enter
        input_box = self.chat_container.get_widget_by_id(
            self.chat_container.ID_INPUT_BOX
        )
        if input_box:
            input_box.add_class("drag-over")

    def on_drag_leave(self, event: events.DragLeave) -> None:
        """Handle drag leave event - remove drop zone highlight."""
        event.prevent_default()
        input_box = self.chat_container.get_widget_by_id(
            self.chat_container.ID_INPUT_BOX
        )
        if input_box:
            input_box.remove_class("drag-over")

    @staticmethod
    def process_dropped_files(
        file_paths: list[str],
    ) -> tuple[list[FileAttachment], list[str]]:
        """Process dropped files and return valid attachments and rejected files."""
        valid_attachments = []
        rejected_files = []

        for path in file_paths:
            if AttachmentHandler.is_supported(path):
                try:
                    valid_attachments.append(FileAttachment.from_path(path))
                except Exception:
                    rejected_files.append(path)
            else:
                rejected_files.append(path)

        return valid_attachments, rejected_files
