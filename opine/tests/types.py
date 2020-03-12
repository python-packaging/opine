import unittest
from configparser import RawConfigParser
from io import StringIO
from typing import Dict, List, Union

from parameterized import parameterized

from imperfect import ConfigFile

from ..types import (
    BaseSuggestion,
    BoolWriter,
    DictWriter,
    ListCommaWriter,
    ListCommaWriterCompat,
    ListSemiWriter,
    SectionWriter,
    StrWriter,
)


class WriterTest(unittest.TestCase):
    @parameterized.expand(  # type: ignore
        [(False,), (True,),]
    )
    def test_bool_writer(self, arg: bool) -> None:
        c = ConfigFile()
        c.set_value("a", "b", BoolWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(str(arg).lower(), rcp["a"]["b"])

    @parameterized.expand(  # type: ignore
        [("hello",), ("a\nb\nc",),]
    )
    def test_str_writer(self, arg: str) -> None:
        c = ConfigFile()
        c.set_value("a", "b", StrWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(arg, rcp["a"]["b"])

    @parameterized.expand(  # type: ignore
        [
            ([], ""),
            (["a"], "\na"),
            (["a", "b"], "\na\nb"),
            (["a", "b", "c"], "\na\nb\nc"),
        ]
    )
    def test_list_comma_writer(self, arg: List[str], expected: str) -> None:
        c = ConfigFile()
        c.set_value("a", "b", ListCommaWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(expected, rcp["a"]["b"])

    @parameterized.expand(  # type: ignore
        [
            ([], ""),
            (["a"], "\na"),
            (["a", "b"], "\na\nb"),
            (["a", "b", "c"], "\na\nb\nc"),
        ]
    )
    def test_list_semi_writer(self, arg: List[str], expected: str) -> None:
        c = ConfigFile()
        c.set_value("a", "b", ListSemiWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(expected, rcp["a"]["b"])

    @parameterized.expand(  # type: ignore
        # fmt: off
        [
            ({}, ""),
            ({"x": "y"}, "\nx=y"),
            ({"x": "y", "z": "zz"}, "\nx=y\nz=zz"),
        ]
        # fmt: on
    )
    def test_dict_writer(self, arg: Dict[str, str], expected: str) -> None:
        c = ConfigFile()
        c.set_value("a", "b", DictWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        # I would prefer this be dangling lines
        self.assertEqual(expected, rcp["a"]["b"])

    @parameterized.expand(  # type: ignore
        # fmt: off
        [
            ([], ""),
            ("abc", "\nabc"),
            (["a"], "\na"),
            (["a", "b"], "\na\nb"),
            (["a", "b", "c"], "\na\nb\nc"),
        ]
        # fmt: on
    )
    def test_list_comma_writer_compat(
        self, arg: Union[str, List[str]], expected: str
    ) -> None:
        c = ConfigFile()
        c.set_value("a", "b", ListCommaWriterCompat().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        # I would prefer this be dangling lines
        self.assertEqual(expected, rcp["a"]["b"])

    @parameterized.expand(  # type: ignore
        [
            ([], ""),
            (["a"], "\na"),
            (["a", "b"], "\na\nb"),
            (["a", "b", "c"], "\na\nb\nc"),
        ]
    )
    def test_section_writer(self, arg: List[str], expected: str) -> None:
        c = ConfigFile()
        c.set_value("a", "b", SectionWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(expected, rcp["a"]["b"])


class BaseSuggestionTest(unittest.TestCase):
    def test_base(self) -> None:
        b = BaseSuggestion()
        with self.assertRaises(NotImplementedError):
            b.check(None)  # type: ignore
        with self.assertRaisesRegex(Exception, "foo"):
            b.skip("foo")
