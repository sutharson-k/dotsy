"""Vercel AI SDK backend for Dotsy.

This module provides integration with the Vercel AI SDK, offering a unified
interface for multiple AI providers through a single consistent API.

The AI SDK supports:
- OpenAI (GPT-4, GPT-3.5-turbo, etc.)
- Anthropic (Claude models)
- Google (Gemini models)
- Mistral AI
- Cohere
- And many more providers through a single interface

Setup:
    1. Install: pip install ai-sdk
    2. Configure provider API keys in environment
    3. Use AI SDK model aliases in Dotsy config

Example Configuration:
    ```toml
    [[providers]]
    name = "aisdk"
    api_style = "aisdk"
    backend = "aisdk"

    [[models]]
    name = "openai:gpt-4o"
    provider = "aisdk"
    alias = "aisdk-gpt-4o"

    [[models]]
    name = "anthropic:claude-sonnet-4-20250514"
    provider = "aisdk"
    alias = "aisdk-claude-sonnet"
    ```
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from dotsy.core.llm.backend.generic import GenericBackend
from dotsy.core.types import LLMMessage, LLMResponse

if TYPE_CHECKING:
    from dotsy.core.config import ModelConfig, ProviderConfig


class AISDKBackend(GenericBackend):
    """Vercel AI SDK backend implementation.

    Uses the AI SDK's unified interface to access multiple providers
    through a single consistent API with automatic provider detection.
    """

    def __init__(
        self,
        model: ModelConfig,
        provider: ProviderConfig,
        **kwargs: Any,
    ) -> None:
        """Initialize AI SDK backend.

        Args:
            model: Model configuration
            provider: Provider configuration (AI SDK uses 'aisdk')
            **kwargs: Additional backend parameters
        """
        super().__init__(model, provider, **kwargs)
        self._client = None
        self._provider_name = self._extract_provider_from_model()

    def _extract_provider_from_model(self) -> str:
        """Extract provider name from model string.

        Model format: "provider:model-name" (e.g., "openai:gpt-4o")
        """
        if ":" in self.model.name:
            return self.model.name.split(":")[0]
        # Default to OpenAI if no provider specified
        return "openai"

    def _get_model_name(self) -> str:
        """Get the actual model name without provider prefix."""
        if ":" in self.model.name:
            return self.model.name.split(":")[1]
        return self.model.name

    def _ensure_client(self) -> None:
        """Initialize AI SDK client if not already done."""
        if self._client is not None:
            return

        try:
            from aisdk import Client

            # AI SDK automatically detects provider from model name
            self._client = Client()
        except ImportError as e:
            raise ImportError(
                "AI SDK not installed. Install with: pip install ai-sdk"
            ) from e

    async def chat_completion(
        self,
        messages: list[LLMMessage],
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> LLMResponse | Any:
        """Generate chat completion using AI SDK.

        Args:
            messages: List of conversation messages
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            tools: List of tool definitions
            **kwargs: Additional provider-specific parameters

        Returns:
            LLMResponse object with completion result
        """
        self._ensure_client()

        model_name = self._get_model_name()
        provider = self._provider_name

        # Prepare messages for AI SDK
        sdk_messages = self._convert_messages(messages)

        # Build generation config
        config: dict[str, Any] = {
            "model": f"{provider}:{model_name}",
            "messages": sdk_messages,
        }

        if temperature is not None:
            config["temperature"] = temperature
        if max_tokens is not None:
            config["max_tokens"] = max_tokens
        if tools:
            config["tools"] = tools

        # Add any provider-specific kwargs
        config.update(kwargs)

        try:
            if stream:
                return await self._stream_completion(config)
            else:
                return await self._single_completion(config)
        except Exception as e:
            raise self._handle_api_error(e) from e

    def _convert_messages(self, messages: list[LLMMessage]) -> list[dict[str, Any]]:
        """Convert Dotsy messages to AI SDK format.

        Args:
            messages: List of LLMMessage objects

        Returns:
            List of message dicts in AI SDK format
        """
        sdk_messages = []
        for msg in messages:
            sdk_msg = {
                "role": msg.role.value,
                "content": msg.content,
            }
            # Add tool calls if present
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                sdk_msg["tool_calls"] = msg.tool_calls
            # Add tool call id for tool responses
            if hasattr(msg, "tool_call_id") and msg.tool_call_id:
                sdk_msg["tool_call_id"] = msg.tool_call_id
            sdk_messages.append(sdk_msg)
        return sdk_messages

    async def _single_completion(
        self, config: dict[str, Any]
    ) -> LLMResponse:
        """Generate a single (non-streaming) completion."""
        from aisdk import generate_text

        result = await generate_text(**config)

        # Convert AI SDK response to Dotsy LLMResponse
        return LLMResponse(
            content=result.text,
            model=self.model.name,
            usage={
                "prompt_tokens": result.usage.prompt_tokens,
                "completion_tokens": result.usage.completion_tokens,
                "total_tokens": result.usage.total_tokens,
            },
            finish_reason=result.finish_reason,
        )

    async def _stream_completion(self, config: dict[str, Any]) -> Any:
        """Generate a streaming completion.

        Returns an async generator yielding response chunks.
        """
        from aisdk import stream_text

        async with stream_text(**config) as stream:
            async for chunk in stream:
                yield chunk

    def _handle_api_error(self, error: Exception) -> Exception:
        """Handle AI SDK API errors and convert to standard exceptions.

        Args:
            error: Original exception from AI SDK

        Returns:
            Appropriate exception for Dotsy to handle
        """
        # Check for common AI SDK error types
        error_type = type(error).__name__

        if error_type == "APICallError":
            return Exception(f"AI SDK API call failed: {error}")
        elif error_type == "InvalidPromptError":
            return Exception(f"Invalid prompt format: {error}")
        elif error_type == "NoObjectGeneratedError":
            return Exception(f"No response generated: {error}")
        elif error_type == "TypeValidationError":
            return Exception(f"Response validation failed: {error}")

        # Default: return original error
        return error

    def is_available(self) -> bool:
        """Check if AI SDK is available and properly configured.

        Returns:
            True if AI SDK is installed and ready to use
        """
        try:
            import aisdk  # noqa: F401

            return True
        except ImportError:
            return False

    def get_provider_info(self) -> dict[str, Any]:
        """Get information about the AI SDK provider.

        Returns:
            Dict with provider details
        """
        return {
            "name": "aisdk",
            "display_name": "Vercel AI SDK",
            "model": self.model.name,
            "provider": self._provider_name,
            "available": self.is_available(),
        }
