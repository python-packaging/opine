# Opine

Most people either hand-write a setup.py, or crib one from someone else.  Either
way, this usually results in not using the most recent features that can make
the job of a distro easier, such as putting the static parts in `setup.cfg`.

This is a kind of linter for packaging, that can suggest changes to your
configuration in {setup.py, setup.cfg, pyproject.toml} for easier consumption by
others.

A related project is [honesty](https://pypi.org/project/honesty/), whose job it
is to make sure that your bdists appear built from the same revision with the
same contents as your sdists are.

# Status

Planning
