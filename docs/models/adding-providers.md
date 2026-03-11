# Adding New Providers

This guide explains how to add a new AI provider to Dotsy.

## Step 1: Add Provider Configuration

Edit `dotsy/core/config.py` and add your provider to `DEFAULT_PROVIDERS`:

```python
ProviderConfig(
    name="your_provider",
    api_base="https://api.your-provider.com/v1",
    api_key_env_var="YOUR_PROVIDER_API_KEY",
    api_style="openai",  # or "anthropic" for Anthropic-style APIs
    backend=Backend.GENERIC,
),
```

## Step 2: Add Models

Add your provider's models to `DEFAULT_MODELS`:

```python
ModelConfig(
    name="your-model-name",
    provider="your_provider",
    alias="your-alias",
    input_price=0.0,
    output_price=0.0,
),
```

## Step 3: Add API Key

Users need to add their API key to `~/.dotsy/.env`:

```
YOUR_PROVIDER_API_KEY=your_actual_api_key_here
```

## Step 4: Update Documentation

Add your provider to:
- `docs/models/providers/README.md`
- `docs/models/README.md`

## API Styles

Dotsy supports two API styles:

### OpenAI-Compatible (`api_style="openai"`)

Most providers use this format:
- `/chat/completions` endpoint
- `Authorization: Bearer {key}` header
- Standard request/response format

### Anthropic (`api_style="anthropic"`)

Anthropic uses a different format:
- `/messages` endpoint
- `x-api-key: {key}` header
- Separate system message parameter

## Testing

After adding a provider:

1. Run `dotsy --setup` to test API key setup
2. Set the provider: `dotsy --provider your_provider --set-api-key YOUR_KEY`
3. Test with: `dotsy -p "Hello!"`

## Example: Adding Sarvam AI

```python
# In DEFAULT_PROVIDERS
ProviderConfig(
    name="sarvam",
    api_base="https://api.sarvam.ai/v1",
    api_key_env_var="SARVAM_API_KEY",
    api_style="openai",
    backend=Backend.GENERIC,
),

# In DEFAULT_MODELS
ModelConfig(
    name="Sarvam-M",
    provider="sarvam",
    alias="sarvam-m",
    input_price=0.0,
    output_price=0.0,
),
```
