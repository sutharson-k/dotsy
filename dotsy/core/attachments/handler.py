from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class FileAttachment(BaseModel):
    """Represents an attached file (image, PDF, etc.) in a message."""

    type: Literal['image', 'pdf', 'text', 'file'] = Field(..., description='File type category')
    mime_type: str = Field(..., description='MIME type of the file')
    file_path: str = Field(..., description='Path to the file')
    file_name: str = Field(..., description='Original file name')
    base64_data: str | None = Field(None, description='Base64 encoded file data (for images)')
    size_bytes: int = Field(default=0, description='File size in bytes')

    @classmethod
    def from_path(cls, file_path: str | Path) -> FileAttachment:
        """Create a FileAttachment from a file path."""
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f'File not found: {path}')

        mime_type, _ = mimetypes.guess_type(str(path))
        if not mime_type:
            mime_type = 'application/octet-stream'

        file_name = path.name
        size_bytes = path.stat().st_size

        # Determine type category
        if mime_type.startswith('image/'):
            attachment_type = 'image'
        elif mime_type == 'application/pdf':
            attachment_type = 'pdf'
        elif mime_type.startswith('text/'):
            attachment_type = 'text'
        else:
            attachment_type = 'file'

        # Encode image data as base64 for API transmission
        base64_data = None
        if attachment_type == 'image':
            with open(path, 'rb') as f:
                base64_data = base64.b64encode(f.read()).decode('utf-8')

        return cls(
            type=attachment_type,
            mime_type=mime_type,
            file_path=str(path),
            file_name=file_name,
            base64_data=base64_data,
            size_bytes=size_bytes,
        )

    def to_message_content(self) -> dict:
        """Convert to message content format for LLM APIs."""
        if self.type == 'image' and self.base64_data:
            return {
                'type': 'image_url',
                'image_url': {
                    'url': f'data:{self.mime_type};base64,{self.base64_data}'
                }
            }
        elif self.type == 'pdf':
            return {
                'type': 'text',
                'text': f'[PDF file: {self.file_name}]'
            }
        elif self.type == 'text':
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    'type': 'text',
                    'text': f'--- {self.file_name} ---\n{content}'
                }
            except Exception:
                return {
                    'type': 'text',
                    'text': f'[Text file: {self.file_name}]'
                }
        else:
            return {
                'type': 'text',
                'text': f'[File: {self.file_name} ({self.mime_type})]'
            }


class AttachmentHandler:
    """Handles drag-and-drop file attachments."""

    SUPPORTED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
    SUPPORTED_PDF_EXTENSIONS = {'.pdf'}
    SUPPORTED_TEXT_EXTENSIONS = {'.txt', '.md', '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.toml', '.xml', '.html', '.css', '.rs', '.go', '.java', '.cpp', '.c', '.h', '.sh', '.bash', '.zsh'}

    @classmethod
    def is_supported(cls, file_path: str | Path) -> bool:
        """Check if a file type is supported for attachment."""
        path = Path(file_path)
        ext = path.suffix.lower()
        return (
            ext in cls.SUPPORTED_IMAGE_EXTENSIONS
            or ext in cls.SUPPORTED_PDF_EXTENSIONS
            or ext in cls.SUPPORTED_TEXT_EXTENSIONS
        )

    @classmethod
    def get_supported_types_description(cls) -> str:
        """Get a human-readable description of supported file types."""
        return (
            f"Images: {', '.join(sorted(cls.SUPPORTED_IMAGE_EXTENSIONS))}\n"
            f"PDFs: {', '.join(sorted(cls.SUPPORTED_PDF_EXTENSIONS))}\n"
            f"Text files: {', '.join(sorted(cls.SUPPORTED_TEXT_EXTENSIONS))}"
        )

    @classmethod
    def process_files(cls, file_paths: list[str | Path]) -> list[FileAttachment]:
        """Process multiple file paths into attachments."""
        attachments = []
        for path in file_paths:
            try:
                if cls.is_supported(path):
                    attachments.append(FileAttachment.from_path(path))
            except Exception:
                continue
        return attachments
