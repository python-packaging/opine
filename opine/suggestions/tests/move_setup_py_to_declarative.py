import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from ...types import Env
from ..move_setup_py_to_declarative import UseDeclarativeConfig


class MoveSetupPyToDeclarativeTest(unittest.TestCase):
    @patch("opine.suggestions.move_setup_py_to_declarative.echo_color_unified_diff")
    def test_one(self, diff: Any) -> None:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "setup.py").write_text(
                "from setuptools import setup\nsetup(name='foo')\n"
            )
            UseDeclarativeConfig().check(Env(Path(d)), True)
            # TODO unsure where the extra newline comes from
            self.assertEqual(
                "[metadata]\nname = foo\n\n", (Path(d) / "setup.cfg").read_text()
            )
            self.assertEqual(
                "from setuptools import setup\nsetup()\n",
                (Path(d) / "setup.py").read_text(),
            )
