import re

from fugle_marketdata import __version__


def test_version():
    # The package version is bumped on every release, so assert it is a
    # well-formed semantic version rather than pinning a specific number.
    assert isinstance(__version__, str)
    assert re.match(r'^\d+\.\d+\.\d+', __version__)
