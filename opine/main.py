import logging
import sys
import traceback
from pathlib import Path
from typing import Optional

import click

from .suggestions import ALL_SUGGESTIONS
from .types import Env

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Show debug output")
@click.option(
    "--autoapply", "-a", is_flag=True, help="Autoapply instead of showing diff"
)
@click.option("--only", help="Just run this one class")
@click.argument("path")
def main(verbose: bool, autoapply: bool, only: Optional[str], path: str) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.ERROR,
        format="%(asctime)-15s %(levelname)-8s %(name)s:%(lineno)s %(message)s",
    )

    env = Env(Path(path))
    rc = 0

    if only:
        selected = [cls for cls in ALL_SUGGESTIONS if cls.__name__ == only]
        if not selected:
            LOG.error(f"Only value {only!r} did not match anything")
            rc |= 2
    else:
        selected = ALL_SUGGESTIONS

    for cls in selected:
        LOG.info(f"Running {cls.__name__}")
        try:
            cls().check(env, autoapply=autoapply)
        except Exception as e:
            rc |= 2
            if verbose:
                traceback.print_exc()
            else:
                print(repr(e))

    sys.exit(rc)


if __name__ == "__main__":  # pragma: no cover
    main()
