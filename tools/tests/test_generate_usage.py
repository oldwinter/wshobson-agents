"""generate.py must print a copyable try line when selection is missing."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
GENERATE = REPO / "tools" / "generate.py"
TRY = "try: python tools/generate.py --harness gemini --plugin python-development"


def run_generate(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GENERATE), *args],
        cwd=REPO,
        capture_output=True,
        text=True,
    )


def test_missing_plugin_prints_try_and_exits_2() -> None:
    proc = run_generate("--harness", "gemini")
    assert proc.returncode == 2
    assert "No --plugin or --all specified" in proc.stderr
    assert TRY in proc.stderr


def test_help_includes_try_example() -> None:
    proc = run_generate("--help")
    assert proc.returncode == 0
    assert TRY in proc.stdout


def test_unknown_plugin_suggests_neighbor_and_try() -> None:
    proc = run_generate("--harness", "gemini", "--plugin", "python-developmnt")
    assert proc.returncode == 1
    assert "plugins/python-developmnt/" in proc.stderr
    assert "python-development" in proc.stderr
    assert TRY in proc.stderr


def test_clean_alone_does_not_require_plugin(tmp_path: Path) -> None:
    proc = run_generate("--harness", "gemini", "--clean", "--output-root", str(tmp_path))
    assert proc.returncode == 0
    assert "Cleaned" in proc.stdout
    assert "No --plugin or --all specified" not in proc.stderr
