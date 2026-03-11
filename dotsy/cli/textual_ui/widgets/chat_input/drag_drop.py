"""Drag-and-drop file handler for DOTSY CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.message import Message

from dotsy.core.attachments.handler import AttachmentHandler, FileAttachment

if TYPE_CHECKING:
    from dotsy.cli.textual_ui.widgets.chat_input.container import ChatInputContainer


class DragDropHandler:
    """Handles drag-and-drop file processing."""

    def __init__(self, chat_container: ChatInputContainer) -> None:
        self.chat_container = chat_container
        self.attachment_handler = AttachmentHandler()

    class FileDropped(Message):
        """Message sent when files are dropped."""

        def __init__(self, file_paths: list[str]) -> None:
            self.file_paths = file_paths
            super().__init__()

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
