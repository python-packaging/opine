from .move_coverage_ini import MoveCoverageIni
from .move_setup_py_to_declarative import UseDeclarativeConfig
from .move_tox_ini import MoveToxIni

ALL_SUGGESTIONS = [
    UseDeclarativeConfig,
    MoveCoverageIni,
    MoveToxIni,
]
