from __future__ import annotations

from dotsy.core.config import Backend
from dotsy.core.llm.backend.dotsy import DotsyBackend
from dotsy.core.llm.backend.generic import GenericBackend
from dotsy.core.llm.backend.modeldev import ModelDevBackend

BACKEND_FACTORY = {
    Backend.DOTSY: DotsyBackend,
    Backend.GENERIC: GenericBackend,
    Backend.MODELDEV: ModelDevBackend,
}
