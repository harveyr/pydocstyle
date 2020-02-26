"""Unit test for pydocstyle utils.

Use tox or py.test to run the test suite.
"""
import re

from pydocstyle import utils


__all__ = ()


def test_common_prefix():
    """Test common prefix length of two strings."""
    assert utils.common_prefix_length('abcd', 'abce') == 3


def test_no_common_prefix():
    """Test common prefix length of two strings that have no common prefix."""
    assert utils.common_prefix_length('abcd', 'cdef') == 0


def test_differ_length():
    """Test common prefix length of two strings differing in length."""
    assert utils.common_prefix_length('abcd', 'ab') == 2


def test_empty_string():
    """Test common prefix length of two strings, one of them empty."""
    assert utils.common_prefix_length('abcd', '') == 0


def test_strip_non_alphanumeric():
    """Test strip of a string leaves only alphanumeric characters."""
    assert utils.strip_non_alphanumeric("  1abcd1...") == "1abcd1"


def test_tokenize():
    """Test tokenize function."""
    result = utils.tokenize("  asdf,  .+1234.*,\n \n  end, ")
    assert result == ["asdf", ".+1234.*", "end"]


def test_get_regexps_from_config_str():
    """Test splitting and compiling of config string into regexps."""
    result = utils.get_regexps_from_config_str(
        "  asdf,  .+1234.*,\n \n  end, "
    )
    assert len(result) == 3
    for regexp in result:
        assert isinstance(regexp, re.Pattern)


def test_is_match():
    """Test matching a filepath against a list of regexps."""
    regexps = utils.get_regexps_from_config_str(
        "  asdf,  .+1234.*,\n \n .*/tests/.*,  end, "
    )
    assert utils.is_match("asdf", regexps)
    assert not utils.is_match("123asdf", regexps)
    assert utils.is_match("/path/to/tests/test_thing.py", regexps)
