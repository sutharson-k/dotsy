# Contributing to Dotsy

Thank you for your interest in Dotsy! We appreciate your support.

## Current Status

**Dotsy is in active development** — our team is iterating quickly and making lots of changes under the hood.

**We especially encourage**:

- **Bug reports** – Help us uncover and squash issues
- **Feedback & ideas** – Tell us what works, what doesn't, and what could be even better
- **Documentation improvements** – Suggest clarity improvements or highlight missing pieces

## How to Provide Feedback

### Bug Reports

If you encounter a bug, please open an issue with the following information:

1. **Description**: A clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - Python version
   - Operating system
   - Dotsy version
6. **Error Messages**: Any error messages or stack traces
7. **Configuration**: Relevant parts of your `config.toml` (redact any sensitive information)

### Feature Requests and Feedback

We'd love to hear your ideas! When submitting feedback or feature requests:

1. **Clear Description**: Explain what you'd like to see or improve
2. **Use Case**: Describe your use case and why this would be valuable
3. **Alternatives**: If applicable, mention any alternatives you've considered

## Development Setup

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) - Modern Python package manager

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/sutharson-k/dotsy.git
   cd dotsy
   ```

2. Install dependencies:

   ```bash
   uv sync --all-extras
   ```

   This will install both runtime and development dependencies.

3. (Optional) Install pre-commit hooks:

   ```bash
   uv run pre-commit install
   ```

   Pre-commit hooks will automatically run checks before each commit.

### Running Tests

Run all tests:

```bash
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest -v
```

Run a specific test file:

```bash
uv run pytest tests/test_agent_tool_call.py
```

### Linting and Type Checking

#### Ruff (Linting and Formatting)

Check for linting issues (without fixing):

```bash
uv run ruff check .
```

Auto-fix linting issues:

```bash
uv run ruff check --fix .
```

Format code:

```bash
uv run ruff format .
```

Check formatting without modifying files (useful for CI):

```bash
uv run ruff format --check .
```

#### Pyright (Type Checking)

Run type checking:

```bash
uv run pyright
```

#### Pre-commit Hooks

Run all pre-commit hooks manually:

```bash
uv run pre-commit run --all-files
```

The pre-commit hooks include:

- Ruff (linting and formatting)
- Pyright (type checking)
- Typos (spell checking)
- YAML/TOML validation
- Action validator (for GitHub Actions)

### Code Style

- **Line length**: 88 characters (Black-compatible)
- **Type hints**: Required for all functions and methods
- **Docstrings**: Follow Google-style docstrings
- **Formatting**: Use Ruff for both linting and formatting
- **Type checking**: Use Pyright (configured in `pyproject.toml`)

See `pyproject.toml` for detailed configuration of Ruff and Pyright.

## Adding Skills

Dotsy supports 145+ specialized skills. To add a custom skill:

1. Create a folder in `~/.dotsy/skills/your-skill-name/`
2. Add a `skill.md` file with YAML frontmatter:

```markdown
---
name: your-skill-name
description: A brief description of what this skill does
---

# Your Skill Name

Detailed instructions for the skill...
```

3. The skill will be available via `/your-skill-name` command

## Adding AI Providers and Models

To add a new AI provider or model:

1. Add the provider to `dotsy/core/config.py` in the `DEFAULT_PROVIDERS` list
2. Add models to the `DEFAULT_MODELS` list
3. Update documentation in `README.md`

See the provider configuration section in `core/config.py` for examples.

## Questions?

If you have questions about using Dotsy, please check the [README](README.md) first. For other inquiries, feel free to open a discussion or issue.

Thank you for helping make Dotsy better! 🙏

— Sutharson
