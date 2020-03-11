import unittest

from .functional import FunctionalTest  # noqa: F401
from .metadata import DistributionTest, EvaluateTest, MetadataTest  # noqa: F401
from .setup_and_metadata import SetupArgsTest  # noqa: F401
from .types import WriterTest  # noqa: F401

unittest.main()
