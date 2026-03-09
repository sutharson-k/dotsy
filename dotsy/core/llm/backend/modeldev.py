"""Models.dev backend for Dotsy.

This module provides integration with models.dev, a unified platform for accessing
200+ AI models from 11+ providers through a single API endpoint.

models.dev offers:
- Unified API for multiple providers (OpenAI, Anthropic, Google, Meta, etc.)
- Simplified billing and API key management
- Automatic model routing and failover
- Consistent interface across different model providers
- Cost optimization through intelligent model selection
- FREE tier available on select providers (Nvidia, iflowcn, modelscope, llama)

Supported Providers (11+):
- evroc, zai, alibaba-coding-plan, zenmux, io-net
- nvidia (FREE), fastrouter, iflowcn (FREE), modelscope (FREE)
- llama (FREE), inference

Setup:
    1. Get API key from https://models.dev
    2. Set MODELSDEV_API_KEY environment variable
    3. Configure models.dev models in Dotsy config

Example Configuration:
    ```toml
    [[providers]]
    name = "modelsdev"
    api_base = "https://api.models.dev/v1"
    api_key_env_var = "MODELSDEV_API_KEY"
    api_style = "openai"
    backend = "modelsdev"

    [[models]]
    name = "gpt-5"
    provider = "modelsdev"
    alias = "modelsdev-gpt-5"
    input_price = 1.25
    output_price = 10.0

    [[models]]
    name = "claude-sonnet-4"
    provider = "modelsdev"
    alias = "modelsdev-claude-sonnet"
    input_price = 3.0
    output_price = 15.0
    ```
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dotsy.core.llm.backend.generic import GenericBackend

if TYPE_CHECKING:
    from dotsy.core.config import ModelConfig, ProviderConfig


class ModelsDevBackend(GenericBackend):
    """Models.dev backend implementation.

    Provides access to 200+ AI models from 11+ providers through models.dev's
    unified API with automatic routing, failover, and cost optimization.
    """

    def __init__(
        self,
        model: ModelConfig,
        provider: ProviderConfig,
        **kwargs: Any,
    ) -> None:
        """Initialize models.dev backend.

        Args:
            model: Model configuration
            provider: Provider configuration (models.dev)
            **kwargs: Additional backend parameters
        """
        super().__init__(model=model, provider=provider, **kwargs)
        self._api_key = None

    def _get_api_key(self) -> str | None:
        """Get models.dev API key from environment."""
        if self._api_key is not None:
            return self._api_key

        import os

        env_var = self.provider.api_key_env_var
        self._api_key = os.getenv(env_var)
        return self._api_key

    def _get_model_name(self) -> str:
        """Get the model name for models.dev API.

        models.dev uses standard model names without provider prefix.
        """
        return self.model.name

    def is_available(self) -> bool:
        """Check if models.dev is available and configured.

        Returns:
            True if API key is set and models.dev is accessible
        """
        api_key = self._get_api_key()
        return api_key is not None and api_key != ""

    def get_provider_info(self) -> dict[str, Any]:
        """Get information about the models.dev provider.

        Returns:
            Dict with provider details
        """
        return {
            "name": "modelsdev",
            "display_name": "Models.dev",
            "model": self.model.name,
            "api_base": self.provider.api_base,
            "available": self.is_available(),
            "total_models": "200+",
            "total_providers": "11+",
            "free_tier": True,
            "features": [
                "Multi-provider access (11+ providers)",
                "Automatic failover and routing",
                "Cost optimization",
                "Unified billing",
                "FREE tier on select providers",
            ],
        }
