import logging

from moreorless.click import echo_color_unified_diff

from imperfect import parse_string

from ..types import BaseSuggestion, Env

LOG = logging.getLogger(__name__)


class MoveCoverageIni(BaseSuggestion):
    # https://coverage.readthedocs.io/en/v4.5.x/config.html
    def check(self, env: Env, autoapply: bool = False) -> None:
        coverage_ini_path = env.base_path / "coverage.ini"
        setup_cfg_path = env.base_path / "setup.cfg"

        if not coverage_ini_path.exists():
            return

        coverage_ini_text = coverage_ini_path.read_text()
        setup_cfg_text = ""
        if setup_cfg_path.exists():
            setup_cfg_text = setup_cfg_path.read_text()

        setup_cfg = parse_string(setup_cfg_text)
        coverage_ini = parse_string(coverage_ini_text)

        for section in coverage_ini.keys():
            # This doesn't iterate and use set_value because that wouldn't
            # preserve comments.
            obj = coverage_ini[section]
            obj.name = f"coverage:{obj.name}"

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
                coverage_ini_path.unlink()
                print("Written")
            else:
                print("Rerun with -a instead to apply")
