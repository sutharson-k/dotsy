---
name: blender-cli
description: Control Blender 3D via CLI-Anything. Create scenes, add objects, apply materials, animate, and render using bash commands. Install first with: pip install -e tools/cli-anything-blender/agent-harness
---

# Blender CLI Tool

Use the bash tool to control Blender via CLI-Anything.

## Setup
```bash
pip install -e tools/cli-anything-blender/agent-harness
```

## Common Commands

### Scene
```bash
python -m cli_anything.blender scene new --name "MyScene"
python -m cli_anything.blender scene status
python -m cli_anything.blender scene save --path output.blend
```

### Objects
```bash
python -m cli_anything.blender object add cube --name "MyCube"
python -m cli_anything.blender object add sphere --name "Ball"
python -m cli_anything.blender object move MyCube --x 1 --y 0 --z 0
python -m cli_anything.blender object scale MyCube --x 2 --y 2 --z 2
python -m cli_anything.blender object list
```

### Materials
```bash
python -m cli_anything.blender material create --name "Red" --color 1,0,0,1
python -m cli_anything.blender material assign Red --object MyCube
```

### Render
```bash
python -m cli_anything.blender render --output render.png --format PNG
```

### JSON output
Add `--json` to any command for structured output.
