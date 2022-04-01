import sys

def test_assignment_increments_ref():
    value = "foobar"

    before = sys.getrefcount(value)
    value2 = value
    after = sys.getrefcount(value)

    assert after == before + 1
    del value2 # unused


def test_del_decrements_ref():
    value = "foobar"
    value2 = value

    before = sys.getrefcount(value)
    del value2
    after = sys.getrefcount(value)

    assert after + 1 == before
