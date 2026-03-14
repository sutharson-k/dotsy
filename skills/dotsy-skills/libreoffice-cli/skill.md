---
name: libreoffice-cli
description: Control LibreOffice via CLI-Anything. Create, edit, and export documents, spreadsheets, and presentations using bash commands. Install first with: pip install -e tools/cli-anything-libreoffice/agent-harness
---

# LibreOffice CLI Tool

Use the bash tool to control LibreOffice via CLI-Anything.

## Setup
```bash
pip install -e tools/cli-anything-libreoffice/agent-harness
```

## Common Commands

```bash
python -m cli_anything.libreoffice open --path document.docx
python -m cli_anything.libreoffice export --path output.pdf --format PDF
python -m cli_anything.libreoffice text insert --content "Hello World"
python -m cli_anything.libreoffice sheet new --name "Sheet1"
python -m cli_anything.libreoffice cell set --ref A1 --value "Data"
```

Add `--json` to any command for structured output.
