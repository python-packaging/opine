## v0.5.1

* No longer unconditionally move `setup_requires`

## v0.5.0

* Handle `setup(keywords=...)` as a string
* Improve tests
* Suggestions
  * move `setup_requires` into `pyproject.toml`

## v0.1.0

* Enough `setup(...)` kwargs recognized to be useful, including some buggy scope
  walking.  Parses `setup_requires` from 99.5% of `setup.py` that I have handy.
* List of suggestions that are performed automatically, with diff or apply mode.
  * move `setup.py` args to `setup.cfg`
  * move `tox.ini` into `setup.cfg`
  * move `coverage.ini` into setup.cfg`

## 0.0.1

* Reserve name
