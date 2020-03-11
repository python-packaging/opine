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

# Usage

```
opine [-a] /path/to/root
```

This will run all suggestions and print a sequence of diffs.  If you want to
apply the changes use `-a`.

# Suggestions

* Move tox.ini to setup.cfg
* Move coverage.ini to setup.cfg
* Move static config from setup.py to setup.cfg

# Status

Beta

# License

opine is copyright [Tim Hatch](http://timhatch.com/), and licensed under
the MIT license.  I am providing code in this repository to you under an open
source license.  This is my personal repository; the license you receive to
my code is from me and not from my employer. See the `LICENSE` file for details.
