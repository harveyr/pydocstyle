"""General shared utilities."""
import ast
import logging
import re
from typing import Iterable, Any, Tuple
from itertools import tee, zip_longest


# Do not update the version manually - it is managed by `bumpversion`.
__version__ = '5.0.3rc'
log = logging.getLogger(__name__)

#: Regular expression for stripping non-alphanumeric characters
NON_ALPHANUMERIC_STRIP_RE = re.compile(r'[\W_]+')


def is_blank(string: str) -> bool:
    """Return True iff the string contains only whitespaces."""
    return not string.strip()


def pairwise(
    iterable: Iterable,
    default_value: Any,
) -> Iterable[Tuple[Any, Any]]:
    """Return pairs of items from `iterable`.

    pairwise([1, 2, 3], default_value=None) -> (1, 2) (2, 3), (3, None)
    """
    a, b = tee(iterable)
    _ = next(b, default_value)
    return zip_longest(a, b, fillvalue=default_value)


def common_prefix_length(a: str, b: str) -> int:
    """Return the length of the longest common prefix of a and b.

    >>> common_prefix_length('abcd', 'abce')
    3

    """
    for common, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            return common
    return min(len(a), len(b))


def strip_non_alphanumeric(string: str) -> str:
    """Strip string from any non-alphanumeric characters."""
    return NON_ALPHANUMERIC_STRIP_RE.sub('', string)


def tokenize(s):
    """Tokenizes a config string by splitting on commas and newlines.

    Returns a list of strings.
    """
    result = []
    lines = s.splitlines()
    for line in lines:
        result += [t.strip() for t in line.split(',') if t.strip()]

    return result


def get_regexps_from_config_str(config_str):
    """Returns list of compiled regexps from the config string.

    Assumes config string is comma-separated patterns, possibly with line
    breaks.
    """
    patterns = tokenize(config_str)
    return [re.compile(p) for p in patterns]


def is_match(filepath, regexps):
    """Returns True if any of the file paths match the given regexps.

    Just a one-liner, broken out for testing.
    """
    return any(e.match(filepath) for e in regexps)
