import logging

from moreorless.click import echo_color_unified_diff
from tomlkit import dumps as toml_dump
from tomlkit import parse as toml_parse
from tomlkit import table

from imperfect import parse_string

from ..types import BaseSuggestion, Env

LOG = logging.getLogger(__name__)


class MoveSetupRequires(BaseSuggestion):
    """
    setup_requires isn't actually enforced before setup.py is run

    This turns it into a PEP 517 build, which can still use setuptools but also
    will ensure that pip (or other tools) install your setup_requires before
    running `setup.py`.
    """

    def check(self, env: Env, autoapply: bool = False) -> None:
        # Does not check setup.py because this comes after
        setup_cfg_path = env.base_path / "setup.cfg"
        pyproject_toml_path = env.base_path / "pyproject.toml"
        if not setup_cfg_path.exists():
            return

        setup_cfg_text = setup_cfg_path.read_text()
        setup_cfg = parse_string(setup_cfg_text)
        try:
            setup_requires = setup_cfg["options"]["setup_requires"]
        except KeyError:
            return

        requires = setup_requires.strip().split("\n")
        if not requires:
            return  # TODO remove the empty item

        pyproject_toml_text = ""
        if pyproject_toml_path.exists():
            pyproject_toml_text = pyproject_toml_path.read_text()
        doc = toml_parse(pyproject_toml_text)
        if "build-system" not in doc:
            doc["build-system"] = table()
        # TODO ensure we're not overwriting
        doc["build-system"]["requires"] = requires
        # TODO upstream deletion to imperfect
        ent = setup_cfg["options"].entries
        for i in range(len(ent)):
            if ent[i].key.lower() == "setup_requires":
                del ent[i]
                break

        echo_color_unified_diff(setup_cfg_text, setup_cfg.text, "setup.cfg")
        echo_color_unified_diff(pyproject_toml_text, toml_dump(doc), "pyproject.toml")
        if autoapply:
            setup_cfg_path.write_text(setup_cfg.text)
            pyproject_toml_path.write_text(toml_dump(doc))
