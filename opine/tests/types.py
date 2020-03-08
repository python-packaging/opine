import unittest
from io import StringIO
from configparser import RawConfigParser

from imperfect import ConfigFile
from parameterized import parameterized

from ..types import StrWriter, ListCommaWriter, ListSemiWriter, DictWriter, BoolWriter

class WriterTest(unittest.TestCase):

    @parameterized.expand([
        (False,),
        (True,),
    ])
    def test_bool_writer(self, arg):
        c = ConfigFile()
        c.set_value("a", "b", BoolWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(str(arg).lower(), rcp["a"]["b"])


    @parameterized.expand([
        ("hello",),
        ("a\nb\nc",),
    ])
    def test_str_writer(self, arg):
        c = ConfigFile()
        c.set_value("a", "b", StrWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(arg, rcp["a"]["b"])

    @parameterized.expand([
        ([], ""),
        (["a"], "\na"),
        (["a", "b"], "\na\nb"),
        (["a", "b", "c"], "\na\nb\nc"),
    ])
    def test_list_comma_writer(self, arg, expected):
        c = ConfigFile()
        c.set_value("a", "b", ListCommaWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(expected, rcp["a"]["b"])

    @parameterized.expand([
        ([], ""),
        (["a"], "\na"),
        (["a", "b"], "\na\nb"),
        (["a", "b", "c"], "\na\nb\nc"),
    ])
    def test_list_semi_writer(self, arg, expected):
        c = ConfigFile()
        c.set_value("a", "b", ListSemiWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        self.assertEqual(expected, rcp["a"]["b"])

    @parameterized.expand([
        ({}, ""),
        ({"x": "y"}, "\nx=y"),
        ({"x": "y", "z": "zz"}, "\nx=y\nz=zz"),
    ])
    def test_dict_writer(self, arg, expected):
        c = ConfigFile()
        c.set_value("a", "b", DictWriter().to_ini(arg))
        buf = StringIO()
        c.build(buf)

        rcp = RawConfigParser(strict=False)
        rcp.read_string(buf.getvalue())
        # I would prefer this be dangling lines
        self.assertEqual(expected, rcp["a"]["b"])


