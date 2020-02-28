from pathlib import Path

import tempfile
import unittest

from opine.metadata import Distribution, from_setup_py

class DistributionTest(unittest.TestCase):
    def test_added_item_in_iter(self):
        d = Distribution()
        d.setup_requires = ["a", "b"]
        self.assertIn("setup_requires", list(d))

class MetadataTest(unittest.TestCase):
    def _read(self, data: str):
        with tempfile.TemporaryDirectory() as d:
            sp = Path(d, "setup.py")
            sp.write_text(data)
            return from_setup_py(Path(d), {})

    def test_smoke(self):
        d = self._read("""\
setup(
    name="foo",
    version="0.1",
)
""")
        self.assertEqual("foo", d.name)
        self.assertEqual("0.1", d.version)

    def test_lists(self):
        d = self._read("""\
setup(
    requires=["a", "b"],
)
""")
        self.assertEqual(["a", "b"], d.requires)

    def test_tuples(self):
        d = self._read("""\
setup(
    requires=("a", "b"),
)
""")
        # TODO: Type
        self.assertEqual(["a", "b"], d.requires)


if __name__ == "__main__":
    unittest.main()
