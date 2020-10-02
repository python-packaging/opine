import unittest

from ..types import BaseSuggestion


class BaseSuggestionTest(unittest.TestCase):
    def test_base(self) -> None:
        b = BaseSuggestion()
        with self.assertRaises(NotImplementedError):
            b.check(None)  # type: ignore
        with self.assertRaisesRegex(Exception, "foo"):
            b.skip("foo")
