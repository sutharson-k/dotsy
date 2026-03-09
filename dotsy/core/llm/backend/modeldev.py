"""Model.dev backend for Dotsy.

This module provides integration with model.dev, a unified platform for accessing
multiple AI models through a single API endpoint.

model.dev offers:
- Unified API for multiple providers
- Simplified billing and API key management
- Automatic model routing and failover
- Consistent interface across different model providers
- Cost optimization through intelligent model selection

Setup:
    1. Get API key from https://model.dev
    2. Set MODELDEV_API_KEY environment variable
    3. Configure model.dev models in Dotsy config

Example Configuration:
    ```toml
    [[providers]]
    name = "modeldev"
    api_base = "https://api.model.dev/v1"
    api_key_env_var = "MODELDEV_API_KEY"
    api_style = "openai"
    backend = "modeldev"

    [[models]]
    name = "gpt-4o"
    provider = "modeldev"
    alias = "modeldev-gpt-4o"
    input_price = 5.0
    output_price = 15.0

    [[models]]
    name = "claude-sonnet-4-20250514"
    provider = "modeldev"
    alias = "modeldev-claude-sonnet"
    input_price = 3.0
    output_price = 15.0
    ```
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dotsy.core.llm.backend.generic import GenericBackend

if TYPE_CHECKING:
    from dotsy.core.config import ModelConfig, ProviderConfig


class ModelDevBackend(GenericBackend):
    """Model.dev backend implementation.

    Provides access to multiple AI providers through model.dev's unified API
    with automatic routing, failover, and cost optimization.
    """

    def __init__(
        self,
        model: ModelConfig,
        provider: ProviderConfig,
        **kwargs: Any,
    ) -> None:
        """Initialize model.dev backend.

        Args:
            model: Model configuration
            provider: Provider configuration (model.dev)
            **kwargs: Additional backend parameters
        """
        super().__init__(model, provider, **kwargs)
        self._api_key = None

    def _get_api_key(self) -> str | None:
        """Get model.dev API key from environment."""
        if self._api_key is not None:
            return self._api_key

        import os

        env_var = self.provider.api_key_env_var
        self._api_key = os.getenv(env_var)
        return self._api_key

    def _get_model_name(self) -> str:
        """Get the model name for model.dev API.

        model.dev uses standard model names without provider prefix.
        """
        return self.model.name

    def is_available(self) -> bool:
        """Check if model.dev is available and configured.

        Returns:
            True if API key is set and model.dev is accessible
        """
        api_key = self._get_api_key()
        return api_key is not None and api_key != ""

    def get_provider_info(self) -> dict[str, Any]:
        """Get information about the model.dev provider.

        Returns:
            Dict with provider details
        """
        return {
            "name": "modeldev",
            "display_name": "Model.dev",
            "model": self.model.name,
            "api_base": self.provider.api_base,
            "available": self.is_available(),
            "features": [
                "Multi-provider access",
                "Automatic failover",
                "Cost optimization",
                "Unified billing",
            ],
        }
