import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, List
from unittest.mock import patch

import libcst as cst
from libcst.metadata import ParentNodeProvider, ScopeProvider
from parameterized import parameterized

from opine.metadata import Distribution, SetupCallAnalyzer, from_setup_py, main


class DistributionTest(unittest.TestCase):
    def test_added_item_in_iter(self) -> None:
        d = Distribution()
        d.setup_requires = ["a", "b"]
        self.assertIn("setup_requires", list(d))


class MetadataTest(unittest.TestCase):
    def _read(self, data: str) -> Distribution:
        with tempfile.TemporaryDirectory() as d:
            sp = Path(d, "setup.py")
            sp.write_text(data)
            return from_setup_py(Path(d), {})

    def test_smoke(self) -> None:
        d = self._read(
            """\
from setuptools import setup
setup(
    name="foo",
    version="0.1",
)
"""
        )
        self.assertEqual("foo", d.name)
        self.assertEqual("0.1", d.version)

    def test_smoke_as_import(self) -> None:
        d = self._read(
            """\
from setuptools import setup as x
x(
    name="foo",
)
"""
        )
        self.assertEqual("foo", d.name)

    def test_smoke_unknown_fail(self) -> None:
        with self.assertRaises(SyntaxError):
            self._read(
                """\
setup(
    name="foo",
)
"""
            )

    def test_lists(self) -> None:
        d = self._read(
            """\
from setuptools import setup
setup(
    requires=["a", "b"],
)
"""
        )
        self.assertEqual(["a", "b"], d.requires)

    def test_tuples(self) -> None:
        d = self._read(
            """\
from setuptools import setup
setup(
    requires=("a", "b"),
)
"""
        )
        self.assertEqual(("a", "b"), d.requires)

    def test_bool(self) -> None:
        d = self._read(
            """\
from setuptools import setup
setup(
    include_package_data=True,
)
"""
        )
        self.assertEqual(True, d.include_package_data)

    def test_local(self) -> None:
        d = self._read(
            """\
from setuptools import setup
v = "0.1"
setup(
    version=v,
)
"""
        )
        self.assertEqual("0.1", d.version)

    def test_global(self) -> None:
        d = self._read(
            """\
from setuptools import setup
v = "0.1"
def foo():
    setup(
        version=v,
    )
"""
        )
        self.assertEqual("0.1", d.version)

    def test_dict(self) -> None:
        d = self._read(
            """\
from setuptools import setup
d = dict(version = "0.1")
def foo():
    setup(**d)
"""
        )
        self.assertEqual("0.1", d.version)


class EvaluateTest(unittest.TestCase):
    @parameterized.expand(  # type: ignore
        [
            ("final = 'x'", "x"),
            ("a='x'; final=a", "x"),
            ("a={'y': 'x'}; final=a['y']", "x"),
        ]
    )
    def test_evaluate(self, input: str, expected: Any) -> None:
        module = cst.parse_module(input)
        analyzer = SetupCallAnalyzer()

        wrapper = cst.MetadataWrapper(module)
        wrapper.visit(analyzer)

        # TODO: MetadataDependent.resolve clears self.metadata
        analyzer.metadata = {
            ScopeProvider: wrapper.resolve(ScopeProvider),
            ParentNodeProvider: wrapper.resolve(ParentNodeProvider),
        }
        # TODO: picks an arbitrary scope
        scope = next(iter(analyzer.metadata[ScopeProvider].values()))
        actual = analyzer.evaluate_in_scope(cst.Name(value="final"), scope)
        self.assertEqual(expected, actual)


class MainTest(unittest.TestCase):
    @patch("opine.metadata.print")
    def test_main(self, print_mock: Any) -> None:
        buf: List[str] = []
        print_mock.side_effect = buf.append
        with tempfile.TemporaryDirectory() as d:
            sp = Path(d, "setup.py")
            sp.write_text(
                "from setuptools import setup\nsetup(setup_requires=['abc'])\n"
            )
            sys.argv = ["main", d]
            main()
        self.assertTrue('"setup_requires": ' in buf[-1])

    @patch("opine.metadata.print")
    @patch("opine.metadata.traceback.print_exc")
    def test_main_fail(self, print_exc_mock: Any, print_mock: Any) -> None:
        buf: List[str] = []
        print_mock.side_effect = lambda x, **kwargs: buf.append(x)
        with tempfile.TemporaryDirectory() as d:
            sp = Path(d, "setup.py")
            sp.write_text("from setuptools import setup\nsetup(setup_requires\n")
            sys.argv = ["main", d]
            main()
        self.assertTrue(buf[-1].startswith("Fail:"))


if __name__ == "__main__":
    unittest.main()
