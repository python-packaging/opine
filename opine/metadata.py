"""
This is mostly compatible with pkginfo's metadata classes.
"""

import json
import sys
import logging
import libcst as cst
from typing import Dict, Any

from pathlib import Path
import pkginfo.distribution

LOG = logging.getLogger(__name__)

class Distribution(pkginfo.distribution.Distribution):
    # These are not actually part of the metadata, see PEP 566
    setup_requires = ()

    def _getHeaderAttrs(self):
        # Until I invent a metadata version to include this, do so
        # unconditionally.
        return super()._getHeaderAttrs() + (
            ("Requires-Setup", "setup_requires", True),
        )


# setup(kwarg=) -> Distribution key
MAPPING = {
    'name': 'name',
    'version': 'version',
    'author': 'author',
    'license': 'license',
    'description': 'summary',
    'long_description': 'description',
    'long_description_content_type': 'description_content_type',

    'install_requires': 'requires_dist',
    'requires': 'requires',
}

def from_setup_py(path: Path, markers: Dict[str, Any]) -> Distribution:
    """
    Reads setup.py (and possibly some imports).

    Will not actually "run" the code but will evaluate some conditions based on
    the markers you provide, since much real-world setup.py checks things like
    version, platform, or even `sys.argv` to come up with what it passes to
    `setup()`.

    There should be some other class to read pyproject.toml.

    This needs a path because one day it may need to read other files alongside
    it.
    """

    # TODO: This does not take care of encodings or py2 syntax.
    module = cst.parse_module((path / "setup.py").read_text())

    # TODO: This is not a good example of LibCST integration.  The right way to
    # do this is with a scope provider and transformer, and perhaps multiple
    # passes.

    d = Distribution()
    d.metadata_version = "2.1"

    for stmt in module.children:
        # TODO: This could be a match more clearly
        if (
            isinstance(stmt, cst.SimpleStatementLine)
            and isinstance(stmt.body[0], cst.Expr)
            and isinstance(stmt.body[0].value, cst.Call)
            and isinstance(stmt.body[0].value.func, cst.Name)
            and stmt.body[0].value.func.value == "setup"
        ):
            for arg in stmt.body[0].value.args:
                if isinstance(arg.keyword, cst.Name) and arg.keyword.value in MAPPING:
                    key = arg.keyword.value
                    # TODO generalize this to an eval_in_scope that handles list
                    # comp too
                    if isinstance(arg.value, cst.SimpleString):
                        setattr(d, MAPPING[key], arg.value.evaluated_value)
                    elif isinstance(arg.value, (cst.Tuple, cst.List)):
                        lst = []
                        for el in arg.value.elements:
                            if isinstance(el.value, cst.SimpleString):
                                lst.append(el.value.evaluated_value)
                            else:
                                LOG.warning(f"Non-SimpleString {el!r}")
                        setattr(d, MAPPING[key], lst)
                    else:
                        LOG.warning(f"Want to store {key!r} but type is {type(arg.value)}")
            break
    else:
        # TODO: Should also warn when more than one
        raise SyntaxError("No simple setup() call found")

    return d

def main():
    dist = from_setup_py(Path(sys.argv[1]), {})
    print(json.dumps({k: getattr(dist, k) for k in list(dist) if getattr(dist,
    k)}, indent=2))

if __name__ == "__main__":
    main()
