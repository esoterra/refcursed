import pytest
import sys
from refcursed import expect_ref_delta

def test_expect_ref_delta():
    with expect_ref_delta(True, delta=0):
        pass

    l = []
    with expect_ref_delta(True, delta=1):
        l.append(True)

def test_expect_ref_delta_on_int():
    with expect_ref_delta(201, delta=0):
        pass

    l = []
    with expect_ref_delta(201, delta=1):
        l.append(201)


def test_expect_ref_delta_does_not_increment_refs():
    before = sys.getrefcount(True)

    l = []
    with expect_ref_delta(True, delta=1):
        l.append(True)

    after = sys.getrefcount(True)
    assert before + 1 == after


def test_expect_ref_delta_wrong():
    with pytest.raises(AssertionError):
        with expect_ref_delta(True, delta=1):
            pass

    with pytest.raises(AssertionError):
        l = []
        with expect_ref_delta(True, delta=2):
            l.append(True)