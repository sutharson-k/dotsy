"""Provider Connection Manager for Dotsy.

Manages connections to 75+ LLM providers through AI SDK and Models.dev.
Handles authentication, model discovery, and provider switching.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from logging import getLogger

from dotsy.core.config import Backend, DotsyConfig, ProviderConfig, ModelConfig
from dotsy.core.paths.config_paths import CONFIG_FILE

logger = getLogger("dotsy")


# Supported providers with their AI SDK packages and configuration
SUPPORTED_PROVIDERS = {
    # Major Providers
    "openai": {
        "display_name": "OpenAI",
        "sdk_package": "@ai-sdk/openai",
        "api_key_env": "OPENAI_API_KEY",
        "api_base": "https://api.openai.com/v1",
        "models_endpoint": "https://api.openai.com/v1/models",
        "default_models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "o1-preview"],
    },
    "anthropic": {
        "display_name": "Anthropic",
        "sdk_package": "@ai-sdk/anthropic",
        "api_key_env": "ANTHROPIC_API_KEY",
        "api_base": "https://api.anthropic.com/v1",
        "default_models": ["claude-sonnet-4-20250514", "claude-3-5-sonnet", "claude-3-opus"],
    },
    "google": {
        "display_name": "Google",
        "sdk_package": "@ai-sdk/google",
        "api_key_env": "GOOGLE_API_KEY",
        "api_base": "https://generativelanguage.googleapis.com/v1beta",
        "default_models": ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
    },
    "mistral": {
        "display_name": "Mistral AI",
        "sdk_package": "@ai-sdk/mistral",
        "api_key_env": "MISTRAL_API_KEY",
        "api_base": "https://api.mistral.ai/v1",
        "default_models": ["mistral-large-latest", "mistral-medium-latest", "codestral-latest"],
    },
    
    # Models.dev Providers (via AI SDK)
    "modelsdev": {
        "display_name": "Models.dev",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "MODELSDEV_API_KEY",
        "api_base": "https://api.models.dev/v1",
        "models_endpoint": "https://models.dev/api.json",
        "supports_75_plus": True,
    },
    
    # Local Models
    "ollama": {
        "display_name": "Ollama (Local)",
        "sdk_package": "@ai-sdk/ollama",
        "api_key_env": "",
        "api_base": "http://localhost:11434/v1",
        "is_local": True,
    },
    "lmstudio": {
        "display_name": "LM Studio (Local)",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "",
        "api_base": "http://localhost:1234/v1",
        "is_local": True,
    },
    "llamacpp": {
        "display_name": "Llama.cpp (Local)",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "",
        "api_base": "http://127.0.0.1:8080/v1",
        "is_local": True,
    },
    
    # Additional AI SDK Providers
    "groq": {
        "display_name": "Groq",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "GROQ_API_KEY",
        "api_base": "https://api.groq.com/openai/v1",
        "default_models": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
    },
    "cohere": {
        "display_name": "Cohere",
        "sdk_package": "@ai-sdk/cohere",
        "api_key_env": "COHERE_API_KEY",
        "api_base": "https://api.cohere.ai/v1",
        "default_models": ["command-r-plus", "command-r", "command"],
    },
    "huggingface": {
        "display_name": "Hugging Face",
        "sdk_package": "@ai-sdk/huggingface",
        "api_key_env": "HF_TOKEN",
        "api_base": "https://api-inference.huggingface.co/v1",
    },
    "together": {
        "display_name": "Together AI",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "TOGETHER_API_KEY",
        "api_base": "https://api.together.xyz/v1",
    },
    "anyscale": {
        "display_name": "Anyscale",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "ANYSCALE_API_KEY",
        "api_base": "https://api.endpoints.anyscale.com/v1",
    },
    "deepinfra": {
        "display_name": "DeepInfra",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "DEEPINFRA_API_KEY",
        "api_base": "https://api.deepinfra.com/v1/openai",
    },
    "openrouter": {
        "display_name": "OpenRouter",
        "sdk_package": "@ai-sdk/openai-compatible",
        "api_key_env": "OPENROUTER_API_KEY",
        "api_base": "https://openrouter.ai/api/v1",
        "models_endpoint": "https://openrouter.ai/api/v1/models",
    },
}


class ProviderConnection:
    """Represents a connected provider with its configuration."""
    
    def __init__(
        self,
        provider_id: str,
        api_key: str | None = None,
        api_base: str | None = None,
        is_active: bool = False,
    ) -> None:
        self.provider_id = provider_id
        self.api_key = api_key
        self.api_base = api_base
        self.is_active = is_active
        self.models: list[dict[str, Any]] = []
        
    @property
    def provider_info(self) -> dict[str, Any]:
        """Get provider information."""
        return SUPPORTED_PROVIDERS.get(self.provider_id, {})
    
    @property
    def display_name(self) -> str:
        """Get human-readable provider name."""
        return self.provider_info.get("display_name", self.provider_id)
    
    @property
    def is_local(self) -> bool:
        """Check if this is a local provider."""
        return self.provider_info.get("is_local", False)
    
    @property
    def requires_api_key(self) -> bool:
        """Check if provider requires API key."""
        return bool(self.provider_info.get("api_key_env", ""))
    
    def to_dict(self) -> dict[str, Any]:
        """Serialize connection to dictionary."""
        return {
            "provider_id": self.provider_id,
            "api_key": self.api_key,
            "api_base": self.api_base,
            "is_active": self.is_active,
            "models": self.models,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProviderConnection:
        """Deserialize connection from dictionary."""
        conn = cls(
            provider_id=data["provider_id"],
            api_key=data.get("api_key"),
            api_base=data.get("api_base"),
            is_active=data.get("is_active", False),
        )
        conn.models = data.get("models", [])
        return conn


class ProviderManager:
    """Manages provider connections and model discovery."""
    
    def __init__(self, config: DotsyConfig) -> None:
        self.config = config
        self.connections: dict[str, ProviderConnection] = {}
        self._load_connections()
    
    def _load_connections(self) -> None:
        """Load provider connections from config."""
        # Load from existing providers in config
        for provider in self.config.providers:
            conn = ProviderConnection(
                provider_id=provider.name,
                api_base=provider.api_base,
                is_active=False,
            )
            self.connections[provider.name] = conn
    
    def get_provider_info(self, provider_id: str) -> dict[str, Any]:
        """Get information about a supported provider."""
        if provider_id not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider_id}")
        return SUPPORTED_PROVIDERS[provider_id]
    
    def list_supported_providers(self) -> list[dict[str, Any]]:
        """List all supported providers."""
        return [
            {
                "id": pid,
                "name": info["display_name"],
                "is_local": info.get("is_local", False),
                "requires_key": bool(info.get("api_key_env", "")),
                "supports_75_plus": info.get("supports_75_plus", False),
            }
            for pid, info in SUPPORTED_PROVIDERS.items()
        ]
    
    def list_connected_providers(self) -> list[ProviderConnection]:
        """List all connected providers."""
        return list(self.connections.values())
    
    async def connect_provider(
        self,
        provider_id: str,
        api_key: str | None = None,
        api_base: str | None = None,
    ) -> ProviderConnection:
        """Connect to a provider and fetch available models."""
        if provider_id not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider_id}. "
                f"Supported: {list(SUPPORTED_PROVIDERS.keys())}"
            )
        
        provider_info = SUPPORTED_PROVIDERS[provider_id]
        
        # Use provided values or defaults
        if api_base is None:
            api_base = provider_info.get("api_base", "")
        
        # For local providers, no API key needed
        if not provider_info.get("is_local", False):
            if api_key is None:
                api_key_env = provider_info.get("api_key_env", "")
                if api_key_env:
                    import os
                    api_key = os.getenv(api_key_env)
        
        # Create connection
        conn = ProviderConnection(
            provider_id=provider_id,
            api_key=api_key,
            api_base=api_base,
            is_active=True,
        )
        
        # Fetch available models
        await self._fetch_models(conn)
        
        # Store connection
        self.connections[provider_id] = conn
        
        # Save to config
        await self._save_to_config(conn)
        
        return conn
    
    async def _fetch_models(self, conn: ProviderConnection) -> None:
        """Fetch available models from provider."""
        provider_info = conn.provider_info
        
        # Special handling for Models.dev
        if conn.provider_id == "modelsdev":
            await self._fetch_modelsdev_models(conn)
            return
        
        # Special handling for local providers
        if conn.provider_info.get("is_local", False):
            await self._fetch_local_models(conn)
            return
        
        # Try to fetch from models endpoint
        models_endpoint = provider_info.get("models_endpoint")
        if models_endpoint:
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(models_endpoint)
                    if response.status_code == 200:
                        data = response.json()
                        conn.models = self._parse_models_response(data, conn.provider_id)
                        return
            except Exception as e:
                logger.warning(f"Failed to fetch models from {models_endpoint}: {e}")
        
        # Fallback to default models
        default_models = provider_info.get("default_models", [])
        conn.models = [
            {"id": model, "name": model, "provider": conn.provider_id}
            for model in default_models
        ]
    
    async def _fetch_modelsdev_models(self, conn: ProviderConnection) -> None:
        """Fetch models from Models.dev API."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get("https://models.dev/api.json")
                if response.status_code == 200:
                    data = response.json()
                    conn.models = []
                    
                    # Parse all providers from Models.dev
                    for provider_id, provider_data in data.items():
                        if isinstance(provider_data, dict) and "models" in provider_data:
                            for model_id, model_data in provider_data["models"].items():
                                conn.models.append({
                                    "id": model_id,
                                    "name": model_data.get("name", model_id),
                                    "provider": "modelsdev",
                                    "family": model_data.get("family", provider_id),
                                    "cost": model_data.get("cost", {}),
                                    "context": model_data.get("limit", {}).get("context", 0),
                                    "is_free": model_data.get("cost", {}).get("input", 0) == 0,
                                })
        except Exception as e:
            logger.warning(f"Failed to fetch Models.dev models: {e}")
            # Fallback to sample models
            conn.models = [
                {"id": "gpt-5", "name": "GPT-5", "provider": "modelsdev"},
                {"id": "claude-sonnet-4", "name": "Claude Sonnet 4", "provider": "modelsdev"},
                {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro", "provider": "modelsdev"},
            ]
    
    async def _fetch_local_models(self, conn: ProviderConnection) -> None:
        """Fetch models from local provider."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{conn.api_base}/models")
                if response.status_code == 200:
                    data = response.json()
                    conn.models = self._parse_models_response(data, conn.provider_id)
        except Exception as e:
            logger.debug(f"Failed to fetch local models: {e}")
            conn.models = []
    
    def _parse_models_response(
        self,
        data: dict[str, Any],
        provider_id: str,
    ) -> list[dict[str, Any]]:
        """Parse models API response."""
        models = []
        
        # OpenAI-style response
        if "data" in data:
            for item in data["data"]:
                if isinstance(item, dict):
                    models.append({
                        "id": item.get("id", ""),
                        "name": item.get("name", item.get("id", "")),
                        "provider": provider_id,
                    })
        # Direct list
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    models.append({
                        "id": item.get("id", item.get("name", "")),
                        "name": item.get("name", item.get("id", "")),
                        "provider": provider_id,
                    })
        # Nested models key
        elif "models" in data:
            for model_id, model_data in data["models"].items():
                if isinstance(model_data, dict):
                    models.append({
                        "id": model_id,
                        "name": model_data.get("name", model_id),
                        "provider": provider_id,
                    })
        
        return models
    
    async def _save_to_config(self, conn: ProviderConnection) -> None:
        """Save provider connection to config."""
        # Check if provider already exists
        existing = next(
            (p for p in self.config.providers if p.name == conn.provider_id),
            None,
        )
        
        if not existing:
            # Add new provider
            provider_info = conn.provider_info
            new_provider = ProviderConfig(
                name=conn.provider_id,
                api_base=conn.api_base or provider_info.get("api_base", ""),
                api_key_env_var=provider_info.get("api_key_env", ""),
                api_style="openai",
                backend=Backend.GENERIC,
            )
            self.config.providers.append(new_provider)
        
        # Save config
        from dotsy.core.paths.config_paths import CONFIG_FILE
        import tomli_w
        
        config_data = {
            "active_model": self.config.active_model,
            "providers": [p.model_dump() for p in self.config.providers],
            "models": [m.model_dump() for m in self.config.models],
        }
        
        CONFIG_FILE.path.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE.path, "wb") as f:
            tomli_w.dump(config_data, f)
    
    def disconnect_provider(self, provider_id: str) -> None:
        """Disconnect a provider."""
        if provider_id in self.connections:
            del self.connections[provider_id]
        logger.info(f"Disconnected provider: {provider_id}")
    
    def set_active_provider(self, provider_id: str) -> None:
        """Set the active provider."""
        if provider_id not in self.connections:
            raise ValueError(f"Provider not connected: {provider_id}")
        
        # Deactivate all
        for conn in self.connections.values():
            conn.is_active = False
        
        # Activate selected
        self.connections[provider_id].is_active = True
    
    def get_active_provider(self) -> ProviderConnection | None:
        """Get the currently active provider."""
        for conn in self.connections.values():
            if conn.is_active:
                return conn
        return None
    
    def get_model(self, model_id: str) -> dict[str, Any] | None:
        """Get model by ID from any connected provider."""
        for conn in self.connections.values():
            for model in conn.models:
                if model["id"] == model_id or f"{conn.provider_id}/{model['id']}" == model_id:
                    return model
        return None
    
    def list_all_models(self) -> list[dict[str, Any]]:
        """List all available models from all connected providers."""
        all_models = []
        for conn in self.connections.values():
            for model in conn.models:
                all_models.append({
                    **model,
                    "full_id": f"{conn.provider_id}/{model['id']}",
                    "provider_name": conn.display_name,
                    "is_local": conn.is_local,
                })
        return all_models


async def get_provider_manager(config: DotsyConfig | None = None) -> ProviderManager:
    """Get or create provider manager."""
    if config is None:
        config = DotsyConfig.load()
    return ProviderManager(config)
