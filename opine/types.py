from dataclasses import dataclass
from pathlib import Path


@dataclass
class Env:
    base_path: Path


class BaseSuggestion:
    def check(self, env: Env, autoapply: bool = False) -> None:
        raise NotImplementedError()

    def skip(self, msg: str) -> None:
        raise Exception(msg)  # TODO
