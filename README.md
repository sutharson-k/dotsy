# Dotsy

[![PyPI Version](https://img.shields.io/pypi/v/dotsy)](https://pypi.org/project/dotsy)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/github/license/yourusername/dotsy)](https://github.com/sutharson-k/dotsy/blob/main/LICENSE)

```
██████╗  ██████╗ ██╗  ██╗
██╔══██╗██╔═══██╗╚██╗██╔╝
██████╔╝██║   ██║ ╚███╔╝
██╔══██╗██║   ██║ ██╔██╗
██║  ██║╚██████╔╝██╔╝ ██╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
```

**Your multi-provider AI coding assistant.**

Dotsy is a powerful command-line coding assistant that supports multiple AI providers including Mistral, OpenAI, Anthropic, Google, and any OpenAI-compatible API. It provides a conversational interface to your codebase, allowing you to explore, modify, and interact with your projects through natural language.

> [!WARNING]
> Dotsy works on Windows, but we officially support and target UNIX environments.

## Features

- **Multi-Provider Support**: Choose from Mistral, OpenAI, Anthropic, Google Gemini, or any OpenAI-compatible API(Use Mistral Api)
- **Interactive Chat**: Conversational AI agent that understands your requests
- **Powerful Toolset**: File manipulation, code search, version control, and command execution
- **Project-Aware Context**: Automatically scans your project structure
- **Multiple Agents**: Different agent profiles for different workflows
- **Highly Configurable**: Customize models, providers, and tool permissions
-**Upcoming Ai Models**:I try to add new ai models such as Ollama for locally runnable models and Groq or Openrouter to access multiple ai models
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
backend = "mistral"

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
```

Or store them in `~/.dotsy/.env`:
```bash
MISTRAL_API_KEY=your-mistral-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
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
