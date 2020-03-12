import io
import logging
from typing import Dict, Optional

import libcst as cst
from moreorless.click import echo_color_unified_diff

import imperfect

from ..metadata import Literal, SetupCallAnalyzer, SetupCallTransformer
from ..setup_and_metadata import SETUP_ARGS
from ..types import BaseSuggestion, Env, SectionWriter

LOG = logging.getLogger(__name__)


class UseDeclarativeConfig(BaseSuggestion):
    def check(self, env: Env, autoapply: bool = False) -> None:
        # TODO: This duplicates some of the logic in
        # opine.metadata.from_setup_py because we don't want a Distribution and
        # want to get the cst object back.

        setup_py = env.base_path / "setup.py"
        if not setup_py.exists():
            return
        module = cst.parse_module(setup_py.read_text())
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
        keywords_to_change: Dict[str, Optional[cst.CSTNode]] = {}
        for k, v in analyzer.saved_args.items():
            # This is a cursory check on the value; really we should get an
            # AlmostTooComplicated or TooComplicated that works well.
            if (
                k in setup_args_dict
                and isinstance(v, Literal)
                and "??" not in str(v.value)
            ):
                LOG.debug(f"{k}: can move {v.value!r}")
                keywords_to_change[k] = None
                if setup_args_dict[k].cfg.writer_cls is SectionWriter:
                    for k2, v2 in v.value.items():
                        cfg.set_value(
                            setup_args_dict[k].cfg.section,
                            k2,
                            setup_args_dict[k].cfg.writer_cls().to_ini(v2),
                        )
                else:
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

        echo_color_unified_diff(cfg_data, buf.getvalue(), "setup.cfg")

        old_code = module.code
        transformer = SetupCallTransformer(
            cst.ensure_type(analyzer.setup_node, cst.Call), keywords_to_change
        )
        new_module = wrapper.visit(transformer)
        new_code = new_module.code

        echo_color_unified_diff(old_code, new_code, "setup.py")

        # TODO validate that the right args got removed
        # print(f"And remove {sorted(keywords_to_change)}")

        if autoapply:
            setup_cfg.write_text(buf.getvalue())
            setup_py.write_text(new_code)
        elif keywords_to_change:
            print("Rerun with -a instead to apply")
