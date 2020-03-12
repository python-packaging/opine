import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from ...types import Env
from ..move_setup_requires import MoveSetupRequires


class MoveSetupRequiresTest(unittest.TestCase):
    @patch("opine.suggestions.move_setup_requires.echo_color_unified_diff")
    def test_one(self, diff: Any) -> None:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "setup.cfg").write_text(
                "[options]\nsetup_requires=\n  foo\n  bar\n"
            )
            MoveSetupRequires().check(Env(Path(d)), True)
            self.assertEqual("[options]\n", (Path(d) / "setup.cfg").read_text())
            self.assertEqual(
                '[build-system]\nrequires = ["foo", "bar"]\n',
                (Path(d) / "pyproject.toml").read_text(),
            )
