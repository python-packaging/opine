import io
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import imperfect
import libcst as cst
import moreorless

from ..metadata import Literal, SetupCallAnalyzer
from ..setup_and_metadata import SETUP_ARGS

LOG = logging.getLogger(__name__)


@dataclass
class Env:
    base_path: Path


class BaseSuggestion:
    def skip(self, msg: str) -> None:
        raise Exception(msg)  # TODO


class UseDeclarativeSuggestion(BaseSuggestion):
    def check(self, env: Env) -> None:
        # TODO: This duplicates some of the logic in
        # opine.metadata.from_setup_py because we don't want a Distribution and
        # want to get the cst object back.

        module = cst.parse_module((env.base_path / "setup.py").read_text())
        analyzer = SetupCallAnalyzer()
        wrapper = cst.MetadataWrapper(module)
        wrapper.visit(analyzer)

        if not analyzer.found_setup:
            self.skip("Could not find setup() call in setup.py")

        setup_cfg = env.base_path / "setup.cfg"
        if setup_cfg.exists():
            cfg_data = setup_cfg.read_text()
        else:
            cfg_data = ""

        cfg = imperfect.parse_string(
            cfg_data + ("\n" if not cfg_data.endswith("\n") else "")
        )
        setup_args_dict = {t.keyword: t for t in SETUP_ARGS}
        keywords_to_remove = set()
        for k, v in analyzer.saved_args.items():
            # This is a cursory check on the value; really we should get an
            # AlmostTooComplicated or TooComplicated that works well.
            if k in setup_args_dict and isinstance(v, Literal) and v.value != "??":
                LOG.debug(f"{k}: can move {v.value!r}")
                keywords_to_remove.add(k)
                cfg.set_value(
                    setup_args_dict[k].cfg.section,
                    setup_args_dict[k].cfg.key,
                    setup_args_dict[k].cfg.writer_cls().to_ini(v.value),
                )
            elif k in setup_args_dict:
                LOG.error(f"{k}: too complicated")
            else:
                LOG.debug(f"{k}: unknown keyword")

        buf = io.StringIO()
        cfg.build(buf)

        print(moreorless.unified_diff(cfg_data, buf.getvalue(), "setup.cfg"))
        print(f"And remove {keywords_to_remove}")


def main(path: str) -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(levelname)-8s %(name)s:%(lineno)s %(message)s",
    )
    UseDeclarativeSuggestion().check(Env(Path(path)))


if __name__ == "__main__":
    main(sys.argv[1])
