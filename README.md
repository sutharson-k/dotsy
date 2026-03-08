# Dotsy

[![PyPI Version](https://img.shields.io/pypi/v/dotsy)](https://pypi.org/project/dotsy)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/github/license/yourusername/dotsy)](https://github.com/sutharson-k/dotsy/blob/main/LICENSE)

```
██████╗ ██████╗ ████████╗███████╗██╗   ██╗
██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝╚██╗ ██╔╝
██║  ██║██║   ██║   ██║   ███████╗ ╚████╔╝
██║  ██║██║   ██║   ██║   ╚════██║  ╚██╔╝
██████╔╝╚██████╔╝   ██║   ███████║   ██║
╚═════╝  ╚═════╝    ╚═╝   ╚══════╝   ╚═╝
```

**Your multi-provider AI coding assistant.**

Dotsy is a powerful command-line coding assistant that supports multiple AI providers including Mistral, OpenAI, Anthropic, Google, and any OpenAI-compatible API. It provides a conversational interface to your codebase, allowing you to explore, modify, and interact with your projects through natural language.

> [!WARNING]
> Dotsy works on Windows, but we officially support and target UNIX environments.

## Features

- **Multi-Provider Support**: Choose from Mistral, OpenAI, Anthropic, Google, Qwen, or any OpenAI-compatible API
- **Interactive Chat**: Conversational AI agent that understands your requests
- **Powerful Toolset**: File manipulation, code search, version control, web search, and command execution
- **Web Search**: DuckDuckGo integration for privacy-focused, no-API-key web search
- **Project-Aware Context**: Automatically scans your project structure
- **Multiple Agents**: Different agent profiles for different workflows
- **Crush CLI Integration**: Seamlessly work with Crush CLI as a coordinated autonomous agent
- **Highly Configurable**: Customize models, providers, and tool permissions
- **Upcoming Ai Models**:I try to add new ai models such as Ollama for locally runnable models and Groq or Openrouter to access multiple ai models
## Quick Start

### Installation

**Using pip:**
```bash
pip install -e .
```

**Using uv:**
```bash
uv tool install --force .
```

### Setup

1. Run the setup command:
```bash
dotsy --setup
```

2. Configure your preferred provider and API key

3. Start using Dotsy:
```bash
dotsy
```

## Supported Providers

Dotsy supports multiple AI providers out of the box:

### Mistral AI
- Models: `devstral-2`, `devstral-small`, `mistral-large`, etc.
- API Key: `MISTRAL_API_KEY`
- Base URL: `https://api.mistral.ai/v1`

### OpenAI
- Models: `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`, etc.
- API Key: `OPENAI_API_KEY`
- Base URL: `https://api.openai.com/v1`

### Anthropic
- Models: `claude-sonnet-4-20250514`, `claude-3-5-sonnet`, `claude-3-opus`, etc.
- API Key: `ANTHROPIC_API_KEY`
- Base URL: `https://api.anthropic.com/v1`

### Google Gemini
- Models: `gemini-2.5-flash`, `gemini-1.5-pro`, etc.
- API Key: `GOOGLE_API_KEY`
- Base URL: `https://generativelanguage.googleapis.com/v1beta`

### Qwen (Alibaba Cloud DashScope)
**Note:** DashScope is currently only available in China. For international users, use Qwen via OpenRouter.

#### China Region:
- Models: `qwen-plus`, `qwen-max`, `qwen-turbo`
- API Key: `DASHSCOPE_API_KEY`
- Base URL: `https://dashscope.aliyuncs.com/compatible-mode/v1`

#### International (via OpenRouter):
- Models: `qwen-72b`, `qwen-coder`
- API Key: `OPENROUTER_API_KEY`
- Base URL: `https://openrouter.ai/api/v1`
- Get API Key: https://openrouter.ai/keys

**Available Qwen Models on OpenRouter:**
- `qwen-72b` - Qwen 2.5 72B Instruct (best overall) ⭐
- `qwen-coder` - Qwen 2.5 Coder 32B Instruct (coding specialized)

#### Groq (Ultra-fast inference):
- Models: `groq-llama`, `groq-llama-8b`, `groq-mixtral`, `groq-gemma`
- API Key: `GROQ_API_KEY`
- Base URL: `https://api.groq.com/openai/v1`
- Get API Key: https://console.groq.com/keys

#### MuleRouter (Qwen Specialized):
- Models: `mule-qwen-plus`, `mule-qwen-max`, `mule-qwen3.5`
- API Key: `MULEROUTER_API_KEY`
- Base URL: `https://api.mulerouter.ai/v1`
- Get API Key: https://www.mulerouter.ai/app/api-keys

**MuleRouter Qwen Models:**
- `mule-qwen3.5` - Qwen 3.5 (latest) ⭐
- `mule-qwen-plus` - Qwen Plus (balanced)
- `mule-qwen-max` - Qwen Max (high performance)

#### Bytez (Qwen3-30B-A3B):
- Models: `bytez-qwen3` (Qwen3-30B-A3B)
- API Key: `BYTEZ_API_KEY`
- Base URL: `https://api.bytez.com/v1`
- Get API Key: https://bytez.ai

**Bytez Model:**
- `bytez-qwen3` - Qwen3 30B A3B (efficient MoE) ⭐

**Groq Models:**
- `groq-llama` - Llama 3.1 70B (free tier)
- `groq-llama-8b` - Llama 3.1 8B (fastest, free tier)
- `groq-mixtral` - Mixtral 8x7B (free tier)
- `groq-gemma` - Gemma2 9B (free tier)

### Custom OpenAI-Compatible APIs
- Any OpenAI-compatible endpoint (LocalAI, Ollama, vLLM, etc.)
- Configurable base URL and API key

## Configuration

Dotsy uses a `~/.dotsy/config.toml` configuration file. Example:

```toml
# Active model alias
active_model = "gpt-4o"

# Theme
textual_theme = "terminal"

# Providers configuration
[[providers]]
name = "openai"
api_base = "https://api.openai.com/v1"
api_key_env_var = "OPENAI_API_KEY"
api_style = "openai"
backend = "generic"

[[providers]]
name = "anthropic"
api_base = "https://api.anthropic.com/v1"
api_key_env_var = "ANTHROPIC_API_KEY"
api_style = "anthropic"
backend = "generic"

[[providers]]
name = "mistral"
api_base = "https://api.mistral.ai/v1"
api_key_env_var = "MISTRAL_API_KEY"
api_style = "openai"
backend = "generic"

# Models configuration
[[models]]
name = "gpt-4o"
provider = "openai"
alias = "gpt-4o"
input_price = 5.0
output_price = 15.0
temperature = 0.2

[[models]]
name = "claude-sonnet-4-20250514"
provider = "anthropic"
alias = "claude-sonnet"
input_price = 3.0
output_price = 15.0
temperature = 0.2

[[models]]
name = "devstral-small-latest"
provider = "mistral"
alias = "devstral-small"
input_price = 0.1
output_price = 0.3
temperature = 0.2
```

## Usage

### Interactive Mode
```bash
dotsy
```

### With Initial Prompt
```bash
dotsy "Refactor the main function to be more modular"
```

### Programmatic Mode
```bash
dotsy --prompt "Analyze the codebase" --output json
```

### Specify Model
Edit your config to change the `active_model` alias.

## Slash Commands

- `/help` - Show help information
- `/compact` - Compact the conversation history
- `/stats` - Show session statistics
- `/reset` - Reset the conversation
- `/tools` - List available tools

## Crush CLI Integration

Dotsy can integrate with [Crush CLI](https://github.com/charmbracelet/crush) to provide enhanced autonomous agent capabilities. Crush CLI acts as a basic CLI assistant while Dotsy coordinates as the autonomous agent.

### Installation

First, install Crush CLI:

```bash
# Homebrew (macOS/Linux)
brew install charmbracelet/tap/crush

# npm
npm install -g @charmland/crush

# Go
go install github.com/charmbracelet/crush@latest

# Windows (Winget)
winget install charmbracelet.crush
```

### Configuration

Enable Crush CLI integration in your `~/.dotsy/config.toml`:

```toml
[crush_cli]
enabled = true
yolo_mode = false  # Set to true to auto-approve all Crush operations
auto_approve_tools = []  # List of tools that don't require approval
disabled_tools = []  # List of tools to disable
config_path = ""  # Optional: path to Crush config file
```

### Available Crush Tools

Once integrated, Dotsy provides these Crush CLI tools:

- **crush_run** - Execute tasks using Crush CLI
- **crush_read_context** - Read project context from AGENTS.md
- **crush_logs** - Retrieve Crush CLI session logs
- **crush_update_providers** - Update Crush CLI provider list

### How It Works

1. **Dotsy as Orchestrator**: Dotsy coordinates complex tasks and can delegate to Crush CLI
2. **Crush as Worker**: Crush CLI executes specific coding tasks with its LLM integration
3. **Shared Context**: Both agents share project context via AGENTS.md
4. **Collaborative Workflow**: Dotsy can analyze Crush's output and provide enhanced responses

### Example Usage

```bash
# Start Dotsy with Crush integration enabled
dotsy

# Ask Dotsy to use Crush for a task
"Use Crush to refactor the authentication module"

# Dotsy will coordinate with Crush CLI to complete the task
```

### Agent Coordination

Dotsy and Crush can work together in different modes:

- **Worker Mode**: Crush executes tasks delegated by Dotsy
- **Orchestrator Mode**: Dotsy coordinates multiple subtasks, some handled by Crush
- **Collaborator Mode**: Both agents contribute to complex tasks


## Environment Variables

Set your API keys using environment variables:

```bash
# Mistral
export MISTRAL_API_KEY="your-mistral-key"

# OpenAI
export OPENAI_API_KEY="your-openai-key"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-key"

# Google
export GOOGLE_API_KEY="your-google-key"

# Qwen (Alibaba Cloud DashScope)
export DASHSCOPE_API_KEY="your-dashscope-key"

# OpenRouter (for Qwen international access)
export OPENROUTER_API_KEY="your-openrouter-key"

# Groq (for ultra-fast inference)
export GROQ_API_KEY="your-groq-key"

# MuleRouter (for Qwen specialized models)
export MULEROUTER_API_KEY="your-mulerouter-key"

# Bytez (for Qwen3-30B-A3B)
export BYTEZ_API_KEY="your-bytez-key"
```

Or store them in `~/.dotsy/.env`:
```bash
MISTRAL_API_KEY=your-mistral-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
DASHSCOPE_API_KEY=your-dashscope-key
OPENROUTER_API_KEY=your-openrouter-key
GROQ_API_KEY=your-groq-key
MULEROUTER_API_KEY=your-mulerouter-key
BYTEZ_API_KEY=your-bytez-key
```

## License

Copyright 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the [LICENSE](LICENSE) file for the full license text.
