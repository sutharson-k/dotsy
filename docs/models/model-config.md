# Model Configuration

Configure which AI model Dotsy uses.

## Configuration File

Models are configured in `~/.dotsy/config.toml`:

```toml
active_model = "devstral-small"
```

## Available Models

See [Providers](providers/README.md) for the full list.

## Changing Models

### Option 1: Edit Config

Edit `~/.dotsy/config.toml`:

```toml
active_model = "your-model-alias"
```

### Option 2: Command Line

Use a different model for a single session:

```bash
dotsy --provider groq -p "Your prompt"
```

## Model Aliases

Aliases are short names for models:

| Alias | Actual Model | Provider |
|-------|-------------|----------|
| `devstral-small` | `codestral-latest` | Mistral |
| `devstral-2` | `mistral-small-latest` | Mistral |
| `groq-llama` | `llama-3.3-70b-versatile` | Groq |
| `gpt-4o` | `gpt-4o` | OpenAI |
| `claude-sonnet` | `claude-sonnet-4-20250514` | Anthropic |
| `sarvam-m` | `Sarvam-M` | Sarvam AI |

## Pricing

Model prices are per 1 million tokens:

- **Input price:** Cost for prompt tokens
- **Output price:** Cost for completion tokens

Free models (like Groq) have $0.0 pricing.

## Token Limits

Different models have different context windows:

- Mistral Small: 32K tokens
- GPT-4 Turbo: 128K tokens
- Claude 3.5 Sonnet: 200K tokens
- Gemini 1.5 Pro: 2M tokens
