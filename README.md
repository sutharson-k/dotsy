# Dotsy

[![PyPI Version](https://img.shields.io/pypi/v/dotsy)](https://pypi.org/project/dotsy)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/github/license/sutharson-k/dotsy)](https://github.com/sutharson-k/dotsy/blob/main/LICENSE)

```
██████╗ ██████╗ ████████╗███████╗██╗   ██╗
██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝╚██╗ ██╔╝
██║  ██║██║   ██║   ██║   ███████╗ ╚████╔╝
██║  ██║██║   ██║   ██║   ╚════██║  ╚██╔╝
██████╔╝╚██████╔╝   ██║   ███████║   ██║
╚═════╝  ╚═════╝    ╚═╝   ╚══════╝   ╚═╝
```

**Your multi-provider AI coding assistant with 145+ specialized skills.**

Dotsy is a powerful command-line coding assistant that supports multiple AI providers including Mistral, OpenAI, Anthropic, Google, and any OpenAI-compatible API. It provides a conversational interface to your codebase, allowing you to explore, modify, and interact with your projects through natural language.

> [!WARNING]
> Dotsy works on Windows, but we officially support and target UNIX environments..

## Features

- **Multi-Provider Support**: Mistral, OpenAI, Anthropic, Google, Qwen, Bytez, Groq, Hugging Face, OpenRouter, or any OpenAI-compatible API
- **145+ Specialized Skills**: From software development to marketing, gaming, content creation, and more
- **Interactive Chat**: Conversational AI agent that understands your requests
- **Bayesian Reasoning**: AI maintains uncertainty, updates beliefs gradually, and shows confidence levels (based on Google Research)
- **Show Thinking**: Toggle AI step-by-step reasoning display with `/thinking` command
- **Powerful Toolset**: File manipulation, code search, version control, web search, and command execution
- **Web Search**: DuckDuckGo integration for privacy-focused, no-API-key web search
- **Browser Automation**: browser-use integration for web testing and interaction
- **Image Support**: Send images with `@/path/to/image.png` syntax for vision analysis
- **Project-Aware Context**: Automatically scans your project structure
- **Multiple Agents**: Different agent profiles for different workflows (Default, Plan, Accept Edits)
- **Highly Configurable**: Customize models, providers, and tool permissions
- **Model Selector UI**: Interactive popup to browse and select models by provider with hover-to-select navigation

## Quick Start

### Installation

**Using npm (Recommended):**
```bash
npm install -g dotsy
```

**Using pip:**
```bash
pip install dotsy

# Install only the providers you need (faster startup):
pip install "dotsy[mistral]"      # Mistral AI (default)
pip install "dotsy[openai]"       # OpenAI / GPT
pip install "dotsy[anthropic]"    # Anthropic / Claude
pip install "dotsy[google]"       # Google Gemini (large install)
pip install "dotsy[browser]"      # Browser automation
pip install "dotsy[computer]"     # Full desktop/system control
pip install "dotsy[all]"          # Everything
```

**Using uv:**
```bash
uv tool install --force .
uv tool install --force "dotsy[all]"   # with all providers
```

### Setup

1. Run the setup command:
```bash
dotsy --setup
```

2. Configure your preferred provider and API key.

3. Start using Dotsy (default model: mistral-large):
```bash
dotsy
```

### Default Model

DOTSY uses **mistral-large** (Mistral AI) by default.

To change the default, edit `~/.dotsy/config.toml`:
```toml
active_model = "gpt-4o"  # or any configured model
```

Or use the model selector in the UI: press the model selection key and browse providers/models with your mouse or arrow keys.

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
- Models: `qwen-72b`, `qwen-coder`, `hunter-alpha`, `healer-alpha`
- API Key: `OPENROUTER_API_KEY`
- Base URL: `https://openrouter.ai/api/v1`
- Get API Key: https://openrouter.ai/keys

**Available Qwen Models on OpenRouter:**
- `qwen-72b` - Qwen 2.5 72B Instruct (best overall) ⭐
- `qwen-coder` - Qwen 2.5 Coder 32B Instruct (coding specialized)

**OpenRouter Specialized Models:**
- `hunter-alpha` - Specialized reasoning model (free, unlimited) ⭐
- `healer-alpha` - Specialized assistance model (free, unlimited) ⭐

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

#### Hugging Face (Uncensored Models):
- Models: `qwen3.5-27b-uncensored` (HauhauCS/Qwen3.5-27B-Uncensored-HauhauCS-Aggressive)
- API Key: `HUGGINGFACE_API_KEY`
- Base URL: `https://api-inference.huggingface.co/v1`
- Get API Key: https://huggingface.co/settings/tokens

**Hugging Face Model:**
- `qwen3.5-27b-uncensored` - Uncensored Qwen 3.5 27B ⭐

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
Edit your config to change the `active_model` alias, or use the interactive model selector in the UI.

### Send Images
Use `@` syntax to attach images for vision analysis:
```bash
@screenshot.png what is in this image?
@C:\Users\You\pic.jpg explain this code
@./diagram.png describe this architecture
```

### Bayesian Reasoning (Default)
DOTSY uses Bayesian reasoning by default - the AI:
- Shows confidence levels (e.g., "I'm 70% confident...")
- Updates beliefs with new evidence
- Accumulates knowledge across conversation
- Explains reasoning process

To disable: add `use_bayesian_reasoning = false` to `~/.dotsy/config.toml`

### Show Thinking (Optional,Some models only have the ability to work with thinking i am trying to add to all the models.bare with me :))
Enable to see AI's step-by-step reasoning before answers:

**Toggle in chat:**
```
/thinking
```

**Or in config:**
```toml
# ~/.dotsy/config.toml
show_thinking = true
```

Output format:
```
<thinking>
1. Analyzing the problem...
2. Considering approach A vs B...
3. Trade-off: A is faster, B is safer...
4. Potential issue: edge case X...
5. Conclusion: use approach A with safeguards
</thinking>

**Final Answer:** [answer here]
```

## Slash Commands

Type `/` in the chat to see all available commands with autocomplete:

| Command | Aliases | Description |
|---------|---------|-------------|
| `/help` | `/help` | Show help information |
| `/config` | `/config`, `/theme` | Edit config settings |
| `/model` | `/model` | Select AI model from popup menu |
| `/reload` | `/reload` | Reload configuration from disk |
| `/clear` | `/clear` | Clear conversation history |
| `/log` | `/log` | Show path to current interaction log file |
| `/compact` | `/compact` | Compact conversation history by summarizing |
| `/exit` | `/exit` | Exit the application |
| `/terminal-setup` | `/terminal-setup` | Configure Shift+Enter for newlines |
| `/status` | `/status` | Display agent statistics |
| `/skills` | `/skills` | List all available skills |
| `/thinking` | `/thinking` | Toggle AI thinking/reasoning display |
| `/set-api-key` | `/set-api-key` | Set API key for a provider |

### Examples

```bash
# Set API key in chat
/set-api-key openai sk-your-api-key-here
/apikey anthropic sk-...
/api-key google AIza...

# View all commands
/help

# Change model (type to search)
/model
# Then type "hunter" or "claude" to filter models
# Use ↑↓ to navigate, Enter to select, or hover and click

# Clear history
/clear
```

## Skills (145+ Specialized Capabilities)

Dotsy includes **145+ specialized skills** covering software development, marketing, content creation, gaming, and more:

### Software Development Skills

- **`/accessibility-auditor`** - WCAG compliance and accessibility testing
- **`/ai-engineer`** - AI/ML system design and implementation
- **`/backend-architect`** - Backend system architecture and design
- **`/code-reviewer`** - Code quality and best practices review
- **`/data-engineer`** - Data pipeline and infrastructure design
- **`/database-optimizer`** - Database performance tuning
- **`/devops-automator`** - CI/CD and infrastructure automation
- **`/frontend-developer`** - Frontend web development
- **`/git-workflow-master`** - Git branching and workflow management
- **`/mcp-builder`** - Model Context Protocol server development
- **`/mobile-app-builder`** - iOS/Android app development
- **`/model-qa-specialist`** - AI model testing and validation
- **`/security-engineer`** - Security assessment and hardening
- **`/senior-developer`** - General software development expertise
- **`/seo-specialist`** - Search engine optimization
- **`/software-architect`** - Software architecture design
- **`/technical-writer`** - Technical documentation
- **`/ui-designer`** - User interface design
- **`/ux-architect`** - User experience architecture
- **`/ux-researcher`** - User research and testing

### Game Development Skills

- **`/blender-add-on-engineer`** - Blender plugin development
- **`/game-audio-engineer`** - Game audio implementation
- **`/game-designer`** - Game mechanics and systems design
- **`/godot-gameplay-scripter`** - Godot engine scripting
- **`/godot-multiplayer-engineer`** - Godot network programming
- **`/godot-shader-developer`** - Godot shader programming
- **`/level-designer`** - Game level design
- **`/narrative-designer`** - Game narrative and storytelling
- **`/roblox-avatar-creator`** - Roblox avatar design
- **`/roblox-experience-designer`** - Roblox game design
- **`/roblox-systems-scripter`** - Roblox Lua scripting
- **`/technical-artist`** - Game art pipeline and tools
- **`/unity-architect`** - Unity system architecture
- **`/unity-editor-tool-developer`** - Unity editor extensions
- **`/unity-multiplayer-engineer`** - Unity networking
- **`/unity-shader-graph-artist`** - Unity shader development
- **`/unreal-multiplayer-architect`** - Unreal Engine networking
- **`/unreal-systems-engineer`** - Unreal Engine systems
- **`/unreal-technical-artist`** - Unreal art pipeline
- **`/unreal-world-builder`** - Unreal level design

### Marketing & Content Skills

- **`/baidu-seo-specialist`** - Baidu search optimization
- **`/bilibili-content-strategist`** - Bilibili video content strategy
- **`/brand-guardian`** - Brand consistency management
- **`/carousel-growth-engine`** - Social carousel content
- **`/content-creator`** - General content creation
- **`/developer-advocate`** - Developer relations content
- **`/douyin-strategist`** - Douyin (TikTok China) strategy
- **`/growth-hacker`** - Growth marketing strategies
- **`/instagram-curator`** - Instagram content strategy
- **`/kuaishou-strategist`** - Kuaishou video strategy
- **`/linkedin-content-creator`** - LinkedIn professional content
- **`/paid-media-auditor`** - Paid advertising audit
- **`/paid-social-strategist`** - Paid social media strategy
- **`/podcast-strategist`** - Podcast production strategy
- **`/ppc-campaign-strategist`** - PPC campaign management
- **`/reddit-community-builder`** - Reddit community engagement
- **`/short-video-editing-coach`** - Short-form video editing
- **`/social-media-strategist`** - Social media strategy
- **`/tiktok-strategist`** - TikTok content strategy
- **`/trend-researcher`** - Trend analysis and research
- **`/twitter-engager`** - Twitter/X engagement strategy
- **`/visual-storyteller`** - Visual narrative design
- **`/wechat-official-account-manager`** - WeChat official account
- **`/weibo-strategist`** - Weibo social strategy
- **`/xiaohongshu-specialist`** - Xiaohongshu (RED) strategy
- **`/zhihu-strategist`** - Zhihu content strategy

### Business & Enterprise Skills

- **`/account-strategist`** - Account management strategy
- **`/accounts-payable-agent`** - AP process automation
- **`/analytics-reporter`** - Business analytics reporting
- **`/compliance-auditor`** - Regulatory compliance audit
- **`/corporate-training-designer`** - Corporate training programs
- **`/deal-strategist`** - Deal negotiation strategy
- **`/document-generator`** - Business document generation
- **`/executive-summary-generator`** - Executive summary creation
- **`/finance-tracker`** - Financial tracking and reporting
- **`/government-digital-presales-consultant`** - GovTech presales
- **`/healthcare-marketing-compliance-specialist`** - Healthcare marketing compliance
- **`/jira-workflow-steward`** - Jira workflow optimization
- **`/legal-compliance-checker`** - Legal compliance verification
- **`/outbound-strategist`** - Outbound sales strategy
- **`/project-shepherd`** - Project coordination
- **`/proposal-strategist`** - Proposal and RFP strategy
- **`/recruitment-specialist`** - Recruitment process optimization
- **`/sales-coach`** - Sales technique coaching
- **`/sales-engineer`** - Sales engineering support
- **`/senior-project-manager`** - Project management expertise
- **`/supply-chain-strategist`** - Supply chain optimization
- **`/support-responder`** - Customer support responses
- **`/workflow-optimizer`** - Business process optimization

### Data & AI Skills

- **`/ai-data-remediation-engineer`** - AI-powered data cleanup
- **`/data-consolidation-agent`** - Data consolidation
- **`/experiment-tracker`** - A/B test tracking
- **`/feedback-synthesizer`** - User feedback synthesis
- **`/identity-graph-operator`** - Customer identity graphs
- **`/image-prompt-engineer`** - Image generation prompts
- **`/lsp-index-engineer`** - Language server indexing
- **`/pipeline-analyst`** - Data pipeline analysis
- **`/sales-data-extraction-agent`** - Sales data extraction
- **`/search-query-analyst`** - Search query analysis
- **`/test-results-analyzer`** - Test result analysis

### Infrastructure & DevOps Skills

- **`/automation-governance-architect`** - Automation governance
- **`/embedded-firmware-engineer`** - Embedded systems development
- **`/evidence-collector`** - Evidence collection automation
- **`/incident-response-commander`** - Incident response coordination
- **`/infrastructure-maintainer`** - Infrastructure maintenance
- **`/sre-site-reliability-engineer`** - Site reliability engineering
- **`/terminal-integration-specialist`** - Terminal integrations
- **`/threat-detection-engineer`** - Threat detection systems

### Specialized Skills

- **`/accessibility-auditor`** - Accessibility compliance
- **`/agentic-identity-trust-architect`** - Digital identity architecture
- **`/agents-orchestrator`** - Multi-agent system orchestration
- **`/app-store-optimizer`** - App store optimization (ASO)
- **`/autonomous-optimization-architect`** - Autonomous system optimization
- **`/behavioral-nudge-engine`** - Behavioral design
- **`/blockchain-security-auditor`** - Blockchain security audit
- **`/book-co-author`** - Book writing collaboration
- **`/china-e-commerce-operator`** - China e-commerce operations
- **`/cross-border-e-commerce-specialist`** - Cross-border e-commerce
- **`/cultural-intelligence-strategist`** - Cultural adaptation strategy
- **`/discovery-coach`** - Discovery process coaching
- **`/feishu-integration-developer`** - Feishu/Lark integrations
- **`/git-workflow-master`** - Git workflow management
- **`/inclusive-visuals-specialist`** - Inclusive visual design
- **`/livestream-commerce-coach`** - Livestream shopping coaching
- **`/macos-spatial-metal-engineer`** - macOS Spatial Computing
- **`/performance-benchmarker`** - Performance benchmarking
- **`/private-domain-operator`** - Private domain traffic
- **`/programmatic-display-buyer`** - Programmatic advertising
- **`/rapid-prototyper`** - Rapid prototyping
- **`/reality-checker`** - Feasibility analysis
- **`/report-distribution-agent`** - Report distribution
- **`/solidity-smart-contract-engineer`** - Solidity smart contracts
- **`/sprint-prioritizer`** - Sprint planning
- **`/studio-operations`** - Studio operations management
- **`/studio-producer`** - Studio production
- **`/study-abroad-advisor`** - Study abroad consulting
- **`/tracking-measurement-specialist`** - Analytics tracking
- **`/visionos-spatial-engineer`** - visionOS development
- **`/whimsy-injector`** - Creative enhancement
- **`/xr-cockpit-interaction-specialist`** - XR cockpit design
- **`/xr-immersive-developer`** - XR immersive experiences
- **`/xr-interface-architect`** - XR interface architecture

### Using Skills

Invoke any skill with its slash command:

```bash
dotsy

# List all available skills
/skills

# Use a specific skill
/code-reviewer
Please review this function for potential improvements...

/security-engineer
Check this code for security vulnerabilities...

/ux-architect
Help me design a better user flow for...
```

### Adding Custom Skills

Skills are stored in `~/.dotsy/skills/` directory. Each skill is a folder containing a `skill.md` file with:
- YAML frontmatter (name, description, settings)
- Markdown content (skill instructions and capabilities)

## CLI-Anything Integration

Dotsy integrates with [CLI-Anything](https://github.com/HKUDS/CLI-Anything) to make desktop software agent-native. Tell dotsy to control Blender, GIMP, OBS, LibreOffice, and more using natural language.

### Supported Apps

| App | Tool Directory | Skill |
|-----|---------------|-------|
| Blender | `tools/cli-anything-blender` | `/blender-cli` |
| GIMP | `tools/cli-anything-gimp` | `/gimp-cli` |
| OBS Studio | `tools/cli-anything-obs` | `/obs-cli` |
| LibreOffice | `tools/cli-anything-libreoffice` | `/libreoffice-cli` |
| Audacity | `tools/cli-anything-audacity` | — |

### Setup

Install the tool harness for the app you want to use:

```bash
# Blender
pip install -e tools/cli-anything-blender/agent-harness

# GIMP
pip install -e tools/cli-anything-gimp/agent-harness

# OBS Studio
pip install -e tools/cli-anything-obs/agent-harness

# LibreOffice
pip install -e tools/cli-anything-libreoffice/agent-harness
```

### Usage

```bash
dotsy

# Activate the skill
/blender-cli

# Now tell dotsy what to do
Create a 3D scene with a red cube at position 0,0,0 and render it to output.png
```

Dotsy will execute the CLI-Anything commands via its bash tool to control the app.

## Crush CLI Integration

Dotsy can integrate with [Crush CLI](https://github.com/charmbracelet/crush) for enhanced autonomous agent capabilities.

### Installation

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

### Enable Integration

Add to `~/.dotsy/config.toml`:

```toml
[crush_cli]
enabled = true
yolo_mode = false  # Set to true to auto-approve all Crush operations
auto_approve_tools = []  # List of tools that don't require approval
disabled_tools = []  # List of tools to disable
```

### Available Crush Tools

| Tool | Description |
|------|-------------|
| `crush_run` | Execute tasks using Crush CLI |
| `crush_read_context` | Read project context from AGENTS.md |
| `crush_logs` | Retrieve Crush CLI session logs |
| `crush_update_providers` | Update Crush CLI provider list |

## Browser Automation

Dotsy supports **browser-use** for web automation:

### Installation

```bash
pip install browser-use
```

browser-use will automatically download Chromium on first run.

### Usage

```bash
dotsy
# "Use browser to open https://example.com"
# "Navigate to github.com and take a screenshot"
# "Click the login button"
```

### Configuration

```toml
# ~/.dotsy/config.toml
[tools.agent_browser]
permission = "ask"  # Always ask before browser actions
headless = true
timeout_seconds = 60
domain_allowlist = ["localhost", "127.0.0.1", "*.yourdomain.com"]
```

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

# OpenRouter (for Qwen international)
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
