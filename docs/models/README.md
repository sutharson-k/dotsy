# Dotsy AI Models & Providers

This documentation covers all AI providers and models supported by Dotsy.

## Quick Links

- [Providers Overview](providers/README.md)
- [Adding New Providers](adding-providers.md)
- [Model Configuration](model-config.md)

## Supported Providers

| Provider | API Base | Key Env Var | Status |
|----------|----------|-------------|--------|
| Mistral AI | https://api.mistral.ai/v1 | MISTRAL_API_KEY | ✅ Built-in |
| OpenAI | https://api.openai.com/v1 | OPENAI_API_KEY | ✅ Built-in |
| Anthropic | https://api.anthropic.com/v1 | ANTHROPIC_API_KEY | ✅ Built-in |
| Google (Gemini) | https://generativelanguage.googleapis.com/v1beta | GOOGLE_API_KEY | ✅ Built-in |
| Groq | https://api.groq.com/openai/v1 | GROQ_API_KEY | ✅ Built-in |
| Sarvam AI | https://api.sarvam.ai/v1 | SARVAM_API_KEY | ✅ Built-in |
| MuleRouter | https://api.mulerouter.ai/v1 | MULEROUTER_API_KEY | ✅ Built-in |
| Bytez | https://api.bytez.com/v1 | BYTEZ_API_KEY | ✅ Built-in |
| OpenRouter | https://openrouter.ai/api/v1 | OPENROUTER_API_KEY | ✅ Built-in |
| LlamaCpp | http://127.0.0.1:8080/v1 | - | ✅ Built-in (Local) |
| Ollama | http://127.0.0.1:11434/v1 | - | ✅ Built-in (Local) |

## Default Active Model

The default active model is `devstral-small` (Mistral's Codestral).

## Adding a New Provider

1. Add provider to `dotsy/core/config.py` in `DEFAULT_PROVIDERS`
2. Add models to `DEFAULT_MODELS`
3. Update this documentation

See [Adding New Providers](adding-providers.md) for detailed steps.
