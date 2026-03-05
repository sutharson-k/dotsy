from __future__ import annotations

from dotsy.core.config import Backend
from dotsy.core.llm.backend.generic import GenericBackend
from dotsy.core.llm.backend.mistral import MistralBackend

BACKEND_FACTORY = {Backend.MISTRAL: MistralBackend, Backend.GENERIC: GenericBackend}
