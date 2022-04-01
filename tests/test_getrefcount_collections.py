import sys

def test_adding_dict_key_increments_ref():
    d = {}
    key = "foobar"

    before = sys.getrefcount(key)
    d[key] = 1
    after = sys.getrefcount(key)

    assert after == before + 1


def test_adding_counter_key_increments_ref():
    from collections import Counter
    c = Counter()
    key = "foobar"

    before = sys.getrefcount(key)
    c[key] = 1
    after = sys.getrefcount(key)

    assert after == before + 1


def test_adding_to_list_increments_ref():
    l = []
    value = "foobar"

    before = sys.getrefcount(value)
    l.append(value)
    after = sys.getrefcount(value)

    assert after == before + 1


def test_clearing_list_decrements_ref():
    value = "foobar"
    l = [value] * 5

    before = sys.getrefcount(value)
    l.clear()
    after = sys.getrefcount(value)

    assert after + 5 == before

