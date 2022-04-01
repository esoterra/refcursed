"""Reference Counting Cursed (refcursed)

# ☠☢ Long-Time Code Danger Warning ☢☠
This comment is a message... and part of a system of messages... pay attention to it!
What is here was dangerous and repulsive to us. This message is a warning about danger.
The danger is still present, in your time, as it was in ours.
The danger is unleashed only if you substantially alter this code.
This code is best shunned and left unused/unchanged.

This package contains various utilities which are all implemented
using the Python runtimes reference counts. In some cases this
allows them to be more efficient or achieve things that would not
otherwise be possible. In all cases this comes at the cost of being
absurd and unadvisable.
"""
import logging
from contextlib import contextmanager
import sys
from typing import Any, List

logger = logging.getLogger(__name__)
logger.warning('You are using the library refcursed, this is not advised. See the included warning.')

_booleans = []

bool

def balance_bool():
    """Achieves balance between True and False.

    Does this by adding True or False to a list until
    the number of True and False references according to
    sys.getrefcount are the same.
    """
    while sys.getrefcount(True) != sys.getrefcount(False):
        if sys.getrefcount(True) < sys.getrefcount(False):
            _booleans.append(True)
        else:
            _booleans.append(False)


@contextmanager
def expect_ref_delta(value: Any, delta: int):
    """A context manager that verifies that the number of references
    to the specified value have changed by the specified amount.
    """
    original = float(sys.getrefcount(value))
    yield
    current = float(sys.getrefcount(value))

    observed_delta = current - original
    if observed_delta != delta:
        raise AssertionError(f'References to {value} changed by {observed_delta}, expected {delta}')


@contextmanager
def expect_ref_deltas(values: List[Any], delta: int):
    """A context manager that verifies that the number of references
    to the specified value have changed by the specified amount.
    """
    original = [float(sys.getrefcount(value)) for value in values]
    yield
    current = [float(sys.getrefcount(value)) for value in values]

    for value, original_count, current_count in zip(values, original, current):
        observed_delta = current_count - original_count
        if observed_delta != delta:
            raise AssertionError(f'References to {value} changed by {observed_delta}, expected {delta}')

def refcounting_sort(values: List[int]):
    """Returns a sorted copy of a list destroying the original.
    This uses the counting sort algorithm.

    Not to be confused with sort_refcount, which sorts values
    by their reference count when the function was called.
    """
    lowest = None
    highest = None

    for value in values:
        if lowest is None or lowest > value:
            lowest = value
        if highest is None or highest < value:
            highest = value

    output = []
    for i in range(lowest, highest+1):
        i_count = float(sys.getrefcount(i))
        for index in range(len(values)):
            if values[index] == i:
                values[index] = None
        i_count = i_count - float(sys.getrefcount(i))
        output.extend([i] * int(i_count))

    return output


def count_values(values: list):
    """Counts the occurrences of each value in a list
    """
    unique_values = set(values)
    counts = { v: float(sys.getrefcount(v)) for v in unique_values }
    values.clear()
    counts = { v: float(1 + counts[v] - sys.getrefcount(v)) for v in unique_values }
    counts = { k: int(v) for k, v, in counts.items() }
    return counts


def sort_refcount(values: list) -> list:
    """
    Not to be confused with refcounting_sort, which is a counting
    sort implementation utilizing sys.getrefcount
    """
    labeled = [(v, float(sys.getrefcount(v))) for v in values]
    return [v for v, _ in sorted(labeled)]


def compare_refcounts(left, right):
    """A function for comparing two values by reference count.

    Safely handles the case where reading the refcount of left
    yields the value right and thus changes its refcount.
    """
    l_count = sys.getrefcount(left)
    r_count = sys.getrefcount(right)

    if l_count == right:
        r_count -= 1

    if l_count < r_count:
        return -1
    elif r_count < l_count:
        return 1
    else:
        return 0
