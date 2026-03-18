---
name: gimp-cli
description: "Control GIMP image editor via CLI-Anything. Open, edit, apply filters, and export images using bash commands. Install first with: pip install -e tools/cli-anything-gimp/agent-harness"
---

# GIMP CLI Tool

Use the bash tool to control GIMP via CLI-Anything.

## Setup
```bash
pip install -e tools/cli-anything-gimp/agent-harness
```

## Common Commands

### Open & Export
```bash
python -m cli_anything.gimp open --path image.png
python -m cli_anything.gimp export --path output.png --format PNG
```

### Edit
```bash
python -m cli_anything.gimp resize --width 1920 --height 1080
python -m cli_anything.gimp crop --x 0 --y 0 --width 800 --height 600
python -m cli_anything.gimp rotate --angle 90
```

### Filters
```bash
python -m cli_anything.gimp filter blur --radius 5
python -m cli_anything.gimp filter sharpen
python -m cli_anything.gimp filter grayscale
```

Add `--json` to any command for structured output.
