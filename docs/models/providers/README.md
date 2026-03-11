# AI Providers

Providers are the API endpoints that Dotsy uses to access AI models.

## Built-in Providers

### Mistral AI

Mistral AI is the default provider for Dotsy.

- **API Base:** `https://api.mistral.ai/v1`
- **API Key Env:** `MISTRAL_API_KEY`
- **Backend:** DOTSY (optimized)
- **Models:**
  - `mistral-small-latest` (alias: `devstral-2`) - $0.4/$2.0 per 1M tokens
  - `codestral-latest` (alias: `devstral-small`) - $0.1/$0.3 per 1M tokens ⭐ Default
  - `mistral-large-latest` (alias: `mistral-large`) - $2.0/$6.0 per 1M tokens

**Get API Key:** https://console.mistral.ai/

---

### OpenAI

- **API Base:** `https://api.openai.com/v1`
- **API Key Env:** `OPENAI_API_KEY`
- **Backend:** GENERIC (OpenAI-compatible)
- **Models:**
  - `gpt-4o` - $5.0/$15.0 per 1M tokens
  - `gpt-4-turbo` - $10.0/$30.0 per 1M tokens
  - `gpt-3.5-turbo` - $0.5/$1.5 per 1M tokens

**Get API Key:** https://platform.openai.com/api-keys

---

### Anthropic

- **API Base:** `https://api.anthropic.com/v1`
- **API Key Env:** `ANTHROPIC_API_KEY`
- **Backend:** GENERIC (Anthropic-specific)
- **Models:**
  - `claude-sonnet-4-20250514` (alias: `claude-sonnet`) - $3.0/$15.0 per 1M tokens
  - `claude-3-5-sonnet-latest` (alias: `claude-3-5-sonnet`) - $3.0/$15.0 per 1M tokens
  - `claude-3-opus-20240229` (alias: `claude-opus`) - $15.0/$75.0 per 1M tokens

**Get API Key:** https://console.anthropic.com/

---

### Google (Gemini)

- **API Base:** `https://generativelanguage.googleapis.com/v1beta`
- **API Key Env:** `GOOGLE_API_KEY`
- **Backend:** GENERIC (OpenAI-compatible)
- **Models:**
  - `gemini-2.0-flash` - $0.1/$0.4 per 1M tokens
  - `gemini-1.5-pro` - $1.25/$5.0 per 1M tokens

**Get API Key:** https://makersuite.google.com/app/apikey

---

### Groq

Groq provides ultra-fast inference for open models.

- **API Base:** `https://api.groq.com/openai/v1`
- **API Key Env:** `GROQ_API_KEY`
- **Backend:** GENERIC (OpenAI-compatible)
- **Models:**
  - `llama-3.3-70b-versatile` (alias: `groq-llama`) - FREE
  - `llama-3.1-8b-instant` (alias: `groq-llama-8b`) - FREE
  - `mixtral-8x7b-32768` (alias: `groq-mixtral`) - FREE
  - `gemma2-9b-it` (alias: `groq-gemma`) - FREE

**Get API Key:** https://console.groq.com/

---

### Sarvam AI

Sarvam AI specializes in Indian language models.

- **API Base:** `https://api.sarvam.ai/v1`
- **API Key Env:** `SARVAM_API_KEY`
- **Backend:** GENERIC (OpenAI-compatible)
- **Models:**
  - `sarvam-m` (alias: `sarvam-m`) - Free tier available
  - `sarvam-30b` - 30B parameter model
  - `sarvam-30b-16k` - 30B with 16K context
  - `sarvam-105b` - 105B parameter model
  - `sarvam-105b-32k` - 105B with 32K context

**Get API Key:** https://platform.sarvam.ai/

**⚠️ Limitations:**
- Does **not** support tool/function calling
- Use for chat-only tasks
- For tool usage, switch to Mistral, OpenAI, or Anthropic

**Features:**
- Optimized for 26+ Indian languages
- Cultural context awareness
- Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia support

---

### MuleRouter

MuleRouter provides access to Qwen models.

- **API Base:** `https://api.mulerouter.ai/v1`
- **API Key Env:** `MULEROUTER_API_KEY`
- **Backend:** GENERIC (OpenAI-compatible)
- **Models:**
  - `qwen/qwen-plus` (alias: `mule-qwen-plus`) - $0.4/$1.2 per 1M tokens
  - `qwen/qwen-max` (alias: `mule-qwen-max`) - $2.4/$9.6 per 1M tokens
  - `qwen/qwen-3-5` (alias: `mule-qwen3.5`) - $0.4/$1.2 per 1M tokens

**Get API Key:** https://mulerouter.com/

---

### Bytez

Bytez is an AI model platform.

- **API Base:** `https://api.bytez.com/v1`
- **API Key Env:** `BYTEZ_API_KEY`
- **Backend:** GENERIC (OpenAI-compatible)
- **Models:**
  - `Qwen/Qwen3-30B-A3B` (alias: `bytez-qwen3`) - $0.15/$0.45 per 1M tokens

**Get API Key:** https://bytez.ai/

---

### OpenRouter

OpenRouter provides access to 100+ models from various providers.

- **API Base:** `https://openrouter.ai/api/v1`
- **API Key Env:** `OPENROUTER_API_KEY`
- **Backend:** GENERIC (OpenAI-compatible)
- **Models:**
  - `qwen/qwen-2.5-72b-instruct` (alias: `qwen-72b`) - $0.18/$0.18 per 1M tokens
  - `qwen/qwen-2.5-coder-32b-instruct` (alias: `qwen-coder`) - $0.18/$0.18 per 1M tokens
  - `google/gemma-3n-e4b-it` (alias: `openrouter-gemma-3n`) - $0.04/$0.12 per 1M tokens
  - `openai/gpt-4o` (alias: `gpt-4o-openrouter`) - $5.0/$15.0 per 1M tokens
  - `anthropic/claude-3-5-sonnet` (alias: `claude-sonnet-openrouter`) - $3.0/$15.0 per 1M tokens
  - `google/gemini-2.0-flash` (alias: `gemini-flash-openrouter`) - $0.1/$0.4 per 1M tokens

**Get API Key:** https://openrouter.ai/

---

### LlamaCpp (Local)

Run Llama models locally.

- **API Base:** `http://127.0.0.1:8080/v1`
- **API Key Env:** (none required)
- **Backend:** GENERIC (OpenAI-compatible)
- **Setup:** Run llama.cpp server locally

---

### Ollama (Local)

Run models locally via Ollama.

- **API Base:** `http://127.0.0.1:11434/v1`
- **API Key Env:** (none required)
- **Backend:** GENERIC (OpenAI-compatible)
- **Setup:** Install Ollama from https://ollama.ai/
