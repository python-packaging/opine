import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Tuple

from click.testing import CliRunner, Result

from ..main import main

SAMPLE_ENV = {
    "setup.py": "from setuptools import setup\nsetup(name='bar')\n",
    "setup.cfg": "[metadata]\nname=foo\n",
    "tox.ini": "[tox]\nenvlist=py36\n\n[testenv]\ncommands=make\n",
    "coverage.ini": "[run]\na=b\n",
}


class FunctionalTest(unittest.TestCase):
    def _run_and_get_output(self, args: List[str]) -> Tuple[Result, Dict[str, str]]:
        with tempfile.TemporaryDirectory() as d:
            td_path = Path(d)
            for filename, contents in SAMPLE_ENV.items():
                (td_path / filename).write_text(contents)

            runner = CliRunner()
            result = runner.invoke(main, args + [d])

            new_contents: Dict[str, str] = {}
            for p in td_path.glob("*.*"):
                new_contents[p.relative_to(td_path).as_posix()] = p.read_text()

        return result, new_contents

    def test_smoke_no_args(self) -> None:
        result, files = self._run_and_get_output([])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(SAMPLE_ENV, files)

    def test_smoke_only_one(self) -> None:
        result, files = self._run_and_get_output(["--only", "MoveToxIni"])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(SAMPLE_ENV, files)

    def test_smoke_write(self) -> None:
        result, files = self._run_and_get_output(["-a"])
        self.assertEqual(0, result.exit_code)
        self.assertNotIn("tox.ini", files)
        self.assertNotIn("coverage.ini", files)

        self.assertEqual(
            """\
from setuptools import setup
setup()
""",
            files["setup.py"],
        )

        self.assertEqual(
            """\
[metadata]
name=bar

[coverage:run]
a=b

[tox:tox]
envlist=py36

[testenv]
commands=make
""",
            files["setup.cfg"],
        )
