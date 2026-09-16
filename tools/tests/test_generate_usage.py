"""generate.py must print a copyable try line when selection is missing."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
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


class GenerateUsageTests(unittest.TestCase):
    def test_missing_plugin_prints_try_and_exits_2(self) -> None:
        proc = run_generate("--harness", "gemini")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("No --plugin or --all specified", proc.stderr)
        self.assertIn(TRY, proc.stderr)

    def test_help_includes_try_example(self) -> None:
        proc = run_generate("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(TRY, proc.stdout)

    def test_unknown_plugin_suggests_neighbor_and_try(self) -> None:
        proc = run_generate("--harness", "gemini", "--plugin", "python-developmnt")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("plugins/python-developmnt/", proc.stderr)
        self.assertIn("python-development", proc.stderr)
        self.assertIn(TRY, proc.stderr)

    def test_clean_alone_does_not_require_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = run_generate("--harness", "gemini", "--clean", "--output-root", tmp)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Cleaned", proc.stdout)
        self.assertNotIn("No --plugin or --all specified", proc.stderr)


if __name__ == "__main__":
    unittest.main()
