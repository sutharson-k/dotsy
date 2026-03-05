from __future__ import annotations

from collections.abc import Callable
import os
from pathlib import Path

from dotsy import DOTSY_ROOT


class GlobalPath:
    def __init__(self, resolver: Callable[[], Path]) -> None:
        self._resolver = resolver

    @property
    def path(self) -> Path:
        return self._resolver()


_DEFAULT_DOTSY_HOME = Path.home() / ".dotsy"


def _get_DOTSY_HOME() -> Path:
    if DOTSY_HOME := os.getenv("DOTSY_HOME"):
        return Path(DOTSY_HOME).expanduser().resolve()
    return _DEFAULT_DOTSY_HOME


DOTSY_HOME = GlobalPath(_get_DOTSY_HOME)
GLOBAL_CONFIG_FILE = GlobalPath(lambda: DOTSY_HOME.path / "config.toml")
GLOBAL_ENV_FILE = GlobalPath(lambda: DOTSY_HOME.path / ".env")
GLOBAL_TOOLS_DIR = GlobalPath(lambda: DOTSY_HOME.path / "tools")
GLOBAL_SKILLS_DIR = GlobalPath(lambda: DOTSY_HOME.path / "skills")
GLOBAL_AGENTS_DIR = GlobalPath(lambda: DOTSY_HOME.path / "agents")
GLOBAL_PROMPTS_DIR = GlobalPath(lambda: DOTSY_HOME.path / "prompts")
SESSION_LOG_DIR = GlobalPath(lambda: DOTSY_HOME.path / "logs" / "session")
TRUSTED_FOLDERS_FILE = GlobalPath(lambda: DOTSY_HOME.path / "trusted_folders.toml")
LOG_DIR = GlobalPath(lambda: DOTSY_HOME.path / "logs")
LOG_FILE = GlobalPath(lambda: DOTSY_HOME.path / "dotsy.log")

DEFAULT_TOOL_DIR = GlobalPath(lambda: DOTSY_ROOT / "core" / "tools" / "builtins")
