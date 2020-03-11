import logging

from moreorless.click import echo_color_unified_diff

from imperfect import parse_string

from ..types import BaseSuggestion, Env

LOG = logging.getLogger(__name__)


class MoveToxIni(BaseSuggestion):
    # https://tox.readthedocs.io/en/latest/config.html
    def check(self, env: Env, autoapply: bool = False) -> None:
        tox_ini_path = env.base_path / "tox.ini"
        setup_cfg_path = env.base_path / "setup.cfg"

        if not tox_ini_path.exists():
            return

        tox_ini_text = tox_ini_path.read_text()
        setup_cfg_text = ""
        if setup_cfg_path.exists():
            setup_cfg_text = setup_cfg_path.read_text()

        setup_cfg = parse_string(setup_cfg_text)
        tox_ini = parse_string(tox_ini_text)

        for section in tox_ini.keys():
            # This doesn't iterate and use set_value because that wouldn't
            # preserve comments.
            obj = tox_ini[section]
            if obj.name == "tox":
                obj.name = "tox:tox"

            if obj.name in setup_cfg:
                LOG.error(f"Section {obj.name!r} already exists in setup.cfg")
            else:
                if obj.leading_whitespace == "" and setup_cfg.sections:
                    obj.leading_whitespace = "\n"
                setup_cfg.sections.append(obj)

        new_text = setup_cfg.text
        if new_text != setup_cfg_text:
            echo_color_unified_diff(setup_cfg_text, new_text, "setup.cfg")
            if autoapply:
                setup_cfg_path.write_text(new_text)
                tox_ini_path.unlink()
                print("Written")
            else:
                print("Rerun with -a instead to apply")
