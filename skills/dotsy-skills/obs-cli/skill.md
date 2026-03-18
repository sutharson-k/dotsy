---
name: obs-cli
description: "Control OBS Studio via CLI-Anything. Start/stop recording, manage scenes, and stream using bash commands. Install first with: pip install -e tools/cli-anything-obs/agent-harness"
---

# OBS Studio CLI Tool

Use the bash tool to control OBS via CLI-Anything.

## Setup
```bash
pip install -e tools/cli-anything-obs/agent-harness
```

## Common Commands

```bash
python -m cli_anything.obs scene list
python -m cli_anything.obs scene switch --name "Gaming"
python -m cli_anything.obs record start
python -m cli_anything.obs record stop
python -m cli_anything.obs stream start
python -m cli_anything.obs stream stop
python -m cli_anything.obs status
```

Add `--json` to any command for structured output.
