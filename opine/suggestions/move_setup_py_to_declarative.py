from pathlib import Path

import libcst as cst

from ..metadata import SetupCallAnalyzer
from ..setup_and_metadata import SETUP_ARGS


class Env:
    base_path: Path


class BaseSuggestion:
    pass


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

        for k, v in analyzer.saved_args.items():
            pass
