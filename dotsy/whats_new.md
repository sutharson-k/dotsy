
## v0.3.0 - New AI Provider Support

### New Providers

- **Sarvam AI** - Indian language models (Hindi, Bengali, Tamil, Telugu, etc.)
  - Model: `Sarvam-M` (alias: `sarvam-m`)
  - API: https://api.sarvam.ai/v1
  - Get key: https://platform.sarvam.ai/

### Documentation

- Added comprehensive models documentation in `docs/models/`
- Provider guides for all 11 supported AI providers
- Configuration guides for adding new providers

### Supported Providers (11 Total)

1. Mistral AI (default)
2. OpenAI
3. Anthropic
4. Google (Gemini)
5. Groq
6. Sarvam AI ⭐ NEW
7. MuleRouter
8. Bytez
9. OpenRouter
10. LlamaCpp (local)
11. Ollama (local)

# What's New

- **Config:** Variables defined in the `.env` file in your global `.vibe` folder now override environment variables
- **Sessions:** Fixed message duplication in persisted sessions
- **Resume:** Only shown when a session is available to resume
