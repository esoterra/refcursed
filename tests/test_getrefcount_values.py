import sys

def test_True_tracks_refs():
    value = True

    before = sys.getrefcount(value)
    l = [value] * 5
    after = sys.getrefcount(value)

    assert after == before + 5
    del l


def test_False_tracks_refs():
    value = False

    before = sys.getrefcount(value)
    l = [value] * 5
    after = sys.getrefcount(value)

    assert after == before + 5
    del l


def test_int_tracks_refs():
    value = 101

    before = sys.getrefcount(value)
    l = [value] * 5
    after = sys.getrefcount(value)

    assert after == before + 5
    del l


def test_float_tracks_refs():
    value = 10.0

    before = sys.getrefcount(value)
    l = [value] * 5
    after = sys.getrefcount(value)

    assert after == before + 5
    del l


def test_ints_intern_and_share_refs():
    l = []
    for i in range(20):
        l.append(i - i) # appends value zero

    for i in l:
        for j in l:
            # asserts that all instances of zero are the same object
            assert i is j
            # asserts that all instances of zero have the same refcount
            assert sys.getrefcount(i) == sys.getrefcount(j)


def test_big_ints_dont_intern():
    l = []
    for i in range(20):
        l.append(_build_int(1, 2, 3, 4, 5)) # appends value 12345

    for i, iv in enumerate(l):
        for j, jv in enumerate(l):
            if i != j:
                # asserts that all instances are different objects
                assert iv is not jv


def test_floats_wont_intern():
    l = []

    for i in range(20):
        l.append(float(i - i))

    for i, iv in enumerate(l):
        for j, jv in enumerate(l):
            if i != j:
                assert iv is not jv


def test_strs_dont_default_intern():
    l = []

    for i in range(20):
        l.append(str(i - i)) # appends value "0"

    for i, iv in enumerate(l):
        for j, jv in enumerate(l):
            if i != j:
                # assert that they are not the same object
                assert iv is not jv


def test_strs_intern_if_sys_intern():
    l = []
    for i in range(20):
        l.append(sys.intern(str(i - i))) # appends value "0" interned

    for outer in l:
        for inner in l:
            # asserts that they are the same object
            assert outer is inner
            # asserts that they have the same refcount
            assert sys.getrefcount(outer) == sys.getrefcount(inner)


def _build_int(*args: int) -> int:
    return sum(v * 10 ** i for i, v in enumerate(reversed(args)))