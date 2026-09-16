"""Quick start must install this fork, not upstream wshobson/agents."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
README = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
FORK = "oldwinter/wshobson-agents"
UPSTREAM = "wshobson/agents"


def _quick_start() -> str:
    match = re.search(r"^## Quick start\n(.*?)(?=^## )", README, flags=re.M | re.S)
    assert match is not None, "README is missing a Quick start section"
    return match.group(1)


def test_readme_identifies_this_fork() -> None:
    intro = README.split("## Quick start", 1)[0]
    assert FORK in intro
    assert "fork" in intro.lower()
    assert UPSTREAM in intro


def test_quick_start_install_commands_use_this_fork() -> None:
    section = _quick_start()
    marketplace = re.findall(r"/plugin marketplace add (\S+)", section)
    codex = re.findall(r"npx codex-marketplace add (\S+)", section)
    clones = re.findall(r"gh repo clone (\S+)", section)

    assert marketplace == [FORK]
    assert codex == [FORK]
    assert clones == [FORK]
    assert f"marketplace add {UPSTREAM}" not in section
    assert f"codex-marketplace add {UPSTREAM}" not in section
    assert f"gh repo clone {UPSTREAM}" not in section
