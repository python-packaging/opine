import configparser
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict

from parameterized import parameterized

from ..setup_and_metadata import SETUP_ARGS
from ..types import ConfigField


def egg_info(files: Dict[str, str]) -> Dict[str, str]:
    # TODO consider
    # https://docs.python.org/3/distutils/apiref.html#distutils.core.run_setup
    # and whether that gives a Distribution that knows setuptools-only options
    with tempfile.TemporaryDirectory() as d:
        for relname, contents in files.items():
            (Path(d) / relname).write_text(contents)
        try:
            # TODO this is very slow.
            subprocess.check_output(
                [sys.executable, "setup.py", "egg_info"],
                cwd=d,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError as e:  # pragma: no cover
            raise Exception(f"Failed to run egg_info: {e.stdout}")

        sources = list(Path(d).rglob("PKG-INFO"))
        assert len(sources) == 1

        c1 = configparser.RawConfigParser(strict=False)
        # TODO figure out what the right api for this is; looks like rfc822
        c1.read_string("[config]\n" + sources[0].read_text())

    return dict(c1["config"])


# These tests do not increase coverage, and just verify that we have the right
# static data.
@unittest.skipIf("SKIP_ARGS_TEST" in os.environ, "SKIP_ARGS_TEST")
class SetupArgsTest(unittest.TestCase):
    @parameterized.expand(  # type: ignore
        [(t,) for t in SETUP_ARGS if t.sample_value is not None]
    )
    def test_arg_mapping(self, field: ConfigField) -> None:
        # Tests that the same arg from setup.py or setup.cfg makes it into
        # metadata in the same way.
        foo = field.sample_value
        setup_py = egg_info(
            {
                "setup.py": "from setuptools import setup\n"
                f"setup({field.keyword}={foo!r})\n"
            }
        )

        setup_cfg = egg_info(
            {
                "setup.cfg": f"[{field.cfg.section}]\n" f"{field.cfg.key} = {foo}\n",
                "setup.py": "from setuptools import setup\n" "setup()\n",
            }
        )

        setup_py_matching_keys = [k for k, v in setup_py.items() if v == str(foo)]
        setup_cfg_matching_keys = [k for k, v in setup_cfg.items() if v == str(foo)]

        if (
            len(setup_py_matching_keys) == 0 or len(setup_cfg_matching_keys) == 0
        ):  # pragma: no cover
            print(setup_py, setup_cfg)

        self.assertEqual(1, len(setup_py_matching_keys), setup_py_matching_keys)
        self.assertEqual(1, len(setup_cfg_matching_keys), setup_cfg_matching_keys)
