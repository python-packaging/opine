from .types import (
    BoolWriter,
    ConfigField,
    DictWriter,
    ListCommaWriter,
    ListCommaWriterCompat,
    ListSemiWriter,
    SectionWriter,
    SetupCfg,
)

# Not all of these are in the metadata, but for ones that are see
# https://packaging.python.org/specifications/core-metadata/ for version added
# and what it means.
SETUP_ARGS = [
    # Metadata 1.0; This ordering is the same as _METHOD_BASENAMES in
    # distutils/dist.py which handles an older version of the metadata.
    # https://docs.python.org/3/distutils/setupscript.html#additional-meta-data
    #
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata
    # does a good job telling you whether it's metadata/options in setup.cfg,
    # but doesn't really tell you what they do or what the metadata keys are or
    # what metadata version they correspond to.
    ConfigField("name", SetupCfg("metadata", "name")),  # Name
    ConfigField("version", SetupCfg("metadata", "version")),  # Version
    ConfigField("author", SetupCfg("metadata", "author")),  # Author
    ConfigField("author_email", SetupCfg("metadata", "author_email")),  # Author-email
    ConfigField("license", SetupCfg("metadata", "license")),  # License
    # TODO license_file, license_files
    ConfigField("url", SetupCfg("metadata", "url")),  # Home-page
    ConfigField("description", SetupCfg("metadata", "description")),  # Summary
    ConfigField(
        "long_description", SetupCfg("metadata", "long_description")
    ),  # Description
    # keywords
    ConfigField(
        "keywords", SetupCfg("metadata", "keywords", writer_cls=ListCommaWriterCompat)
    ),
    # platforms
    # fullname
    # contact
    # contact_email
    # Metadata 1.1, supported by distutils
    # provides
    # requires
    # obsoletes
    ConfigField(
        "classifiers",
        SetupCfg("metadata", "classifiers", writer_cls=ListSemiWriter),
        sample_value=None,
    ),
    # download_url
    # Metadata 1.1
    # supported-platform (binary only?)
    # Metadata 1.2, half-supported by distutils but not written in PKG-INFO
    ConfigField("maintainer", SetupCfg("metadata", "maintainer")),  # Maintainer
    ConfigField(
        "maintainer_email", SetupCfg("metadata", "maintainer_email")
    ),  # Maintainer-email
    # Metadata 1.2, not at all supported by distutils
    ConfigField(
        "python_requires", SetupCfg("options", "python_requires"), sample_value="<4.0"
    ),  # Requires-Python
    # requires_external
    # project_url -> dict
    ConfigField(
        "project_urls",
        SetupCfg("metadata", "project_urls", writer_cls=DictWriter),
        sample_value=None,  # {"Bugtracker": "http://example.com"},
    ),
    # requires_dist
    # provides_dist (rarely used)
    # obsoletes_dist (rarely used)
    # Metadata 2.1
    # text/plain, text/x-rst, text/markdown
    # This allows charset and variant (for markdown, GFM or CommonMark)
    ConfigField(
        "long_description_content_type",
        SetupCfg("metadata", "long_description_content_type"),
    ),  # Description-Content-Type
    # provides_extra
    # Not written to PKG-INFO
    # [options]
    ConfigField(
        "zip_safe",
        SetupCfg("options", "zip_safe", writer_cls=BoolWriter),
        sample_value=None,
    ),
    # zip_safe bool
    ConfigField(
        "setup_requires",
        SetupCfg("options", "setup_requires", writer_cls=ListSemiWriter),
        sample_value=None,
    ),
    ConfigField(
        "install_requires",
        SetupCfg("options", "install_requires", writer_cls=ListSemiWriter),
        sample_value=None,
    ),
    ConfigField(
        "tests_require",
        SetupCfg("options", "tests_require", writer_cls=ListSemiWriter),
        sample_value=None,
    ),
    ConfigField(
        "include_package_data",
        SetupCfg("options", "include_package_data", writer_cls=BoolWriter),
        sample_value=None,  # True,
    ),
    #
    ConfigField(
        "extras_require",
        SetupCfg("options.extras_require", "UNUSED", writer_cls=SectionWriter),
        sample_value=None,
    ),
    # use_2to3
    # use_2to3_fixers list-comma
    # use_2to3_exclude_fixers list-comma
    # convert_2to3_doctests list-comma
    ConfigField(
        "scripts",
        SetupCfg("options", "scripts", writer_cls=ListCommaWriter),
        sample_value=None,
    ),
    # eager_resources list-comma
    # dependency_links list-comma
    ConfigField(
        "packages",
        SetupCfg("options", "packages", writer_cls=ListCommaWriter),
        sample_value=None,
    ),
    ConfigField(
        "package_dir",
        SetupCfg("options", "package_dir", writer_cls=DictWriter),
        sample_value=None,
    ),
    ConfigField(
        "package_data",
        SetupCfg("options.package_data", "UNUSED", writer_cls=SectionWriter),
        sample_value=None,  # {"foo": ["py.typed"]},
    ),
    # package_data (section)
    # exclude_package_data (section)
    ConfigField(
        "namespace_packages",
        SetupCfg("options", "namespace_packages", writer_cls=ListCommaWriter),
        sample_value=None,  # ["foo", "bar"],
    ),
    ConfigField(
        "py_modules",
        SetupCfg("options", "py_modules", writer_cls=ListCommaWriter),
        sample_value=None,
    ),
    ConfigField(
        "data_files",
        SetupCfg("options.data_files", "UNUSED", writer_cls=SectionWriter),
        sample_value=None,
    ),
    #
    # Documented, but not in the table...
    ConfigField("test_suite", SetupCfg("options", "test_suite"), sample_value=None,),
    ConfigField("test_loader", SetupCfg("options", "test_loader"), sample_value=None,),
]
