from setuptools import setup


def parse_version():
    with open("opine/__version__.py") as f:
        data = f.read()
    d = {}
    exec(data, d)
    return d["__version__"]


setup(version=parse_version())
