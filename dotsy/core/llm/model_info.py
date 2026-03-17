"""Fetch real context window sizes from provider APIs.

Supports OpenRouter (covers 300+ models) and falls back to
known hardcoded values for other providers.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

logger = logging.getLogger("dotsy")

# Known context windows for common models (fallback when API unavailable)
KNOWN_CONTEXT_WINDOWS: dict[str, int] = {
    # Mistral
    "devstral-2": 131_072,
    "devstral-small": 131_072,
    "mistral-large": 131_072,
    "mistral-small": 131_072,
    "codestral": 262_144,
    # OpenAI
    "gpt-4o": 128_000,
    "gpt-4-turbo": 128_000,
    "gpt-4": 8_192,
    "gpt-3.5-turbo": 16_385,
    "o1": 200_000,
    "o3": 200_000,
    # Anthropic
    "claude-3-5-sonnet": 200_000,
    "claude-3-opus": 200_000,
    "claude-sonnet-4": 200_000,
    # Google
    "gemini-2.5-flash": 1_000_000,
    "gemini-1.5-pro": 2_000_000,
    "gemini-2.0-flash": 1_000_000,
    # Nvidia Nemotron
    "nemotron": 131_072,
    "nvidia/llama-3.1-nemotron-ultra-253b-v1": 131_072,
    "nvidia/llama-3.3-nemotron-super-49b-v1": 131_072,
    # Qwen
    "qwen-72b": 131_072,
    "qwen-coder": 131_072,
    # Groq
    "groq-llama": 131_072,
    "groq-llama-8b": 131_072,
    "groq-mixtral": 32_768,
    "groq-gemma": 8_192,
    # Defaults by provider
    "_openrouter_default": 32_768,
    "_mistral_default": 131_072,
    "_openai_default": 128_000,
    "_anthropic_default": 200_000,
    "_google_default": 1_000_000,
    "_default": 32_768,
}

# Cache: model_name -> context_window
_CONTEXT_WINDOW_CACHE: dict[str, int] = {}
_OPENROUTER_FETCHED = False


async def _fetch_openrouter_models(api_key: str) -> dict[str, int]:
    """Fetch all model context windows from OpenRouter API."""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            if resp.status_code != 200:
                return {}
            data = resp.json()
            result = {}
            for model in data.get("data", []):
                model_id = model.get("id", "")
                ctx = model.get("context_length") or model.get("top_provider", {}).get("context_length")
                if model_id and ctx:
                    result[model_id] = int(ctx)
            logger.info("Fetched context windows for %d OpenRouter models", len(result))
            return result
    except Exception as e:
        logger.debug("Failed to fetch OpenRouter models: %s", e)
        return {}


async def get_context_window(
    model_name: str,
    model_alias: str,
    provider_name: str,
    api_key: str | None = None,
) -> int:
    """Get the real context window size for a model.

    Priority:
    1. Cache hit
    2. OpenRouter API (if openrouter provider)
    3. Known hardcoded values
    4. Provider default fallback
    """
    global _OPENROUTER_FETCHED

    # Check cache
    cache_key = model_name or model_alias
    if cache_key in _CONTEXT_WINDOW_CACHE:
        return _CONTEXT_WINDOW_CACHE[cache_key]

    # Check hardcoded known values by alias or partial name
    for key, val in KNOWN_CONTEXT_WINDOWS.items():
        if key.startswith("_"):
            continue
        if key in model_name.lower() or key in model_alias.lower():
            _CONTEXT_WINDOW_CACHE[cache_key] = val
            return val

    # Fetch from OpenRouter if applicable
    if provider_name == "openrouter" and api_key and not _OPENROUTER_FETCHED:
        _OPENROUTER_FETCHED = True
        fetched = await _fetch_openrouter_models(api_key)
        _CONTEXT_WINDOW_CACHE.update(fetched)
        if model_name in fetched:
            return fetched[model_name]

    # Provider default fallback
    provider_default_key = f"_{provider_name}_default"
    fallback = KNOWN_CONTEXT_WINDOWS.get(
        provider_default_key,
        KNOWN_CONTEXT_WINDOWS["_default"]
    )
    _CONTEXT_WINDOW_CACHE[cache_key] = fallback
    logger.debug(
        "Using fallback context window %d for model %s", fallback, model_name
    )
    return fallback


def get_safe_compact_threshold(context_window: int, safety_factor: float = 0.80) -> int:
    """Get a safe auto-compact threshold at 80% of the context window.

    This leaves 20% headroom for the compact summary itself,
    preventing the compact loop issue.
    """
    return int(context_window * safety_factor)
