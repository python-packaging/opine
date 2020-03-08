from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type


# These implement the basic types listed at
# https://setuptools.readthedocs.io/en/latest/setuptools.html#specifying-values
class BaseWriter:
    def to_ini(self, value: Any) -> str:  # pragma: no cover
        raise NotImplementedError


class StrWriter(BaseWriter):
    def to_ini(self, value: str) -> str:
        return value


class ListCommaWriter(BaseWriter):
    def to_ini(self, value: List[str]) -> str:
        if not value:
            return ""
        return "".join(f"\n{k}" for k in value)


class ListSemiWriter(BaseWriter):
    def to_ini(self, value: List[str]) -> str:
        if not value:
            return ""
        return "".join(f"\n{k}" for k in value)


class BoolWriter(BaseWriter):
    def to_ini(self, value: bool) -> str:
        return "true" if value else "false"


class DictWriter(BaseWriter):
    def to_ini(self, value: Dict[str, str]) -> str:
        if not value:
            return ""
        return "".join(f"\n{k}={v}" for k, v in value.items())


@dataclass
class SetupCfg:
    section: str
    key: str
    writer_cls: Type[BaseWriter] = StrWriter


@dataclass
class PyProject:
    section: str
    key: str
    # TODO setuptools-only?


@dataclass
class Metadata:
    key: str
    repeated: bool = False


@dataclass
class ConfigField:
    keyword: str
    # TODO type/repeated/etc
    cfg: SetupCfg
    sample_value: Optional[Any] = "foo"
