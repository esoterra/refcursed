from refcursed import expect_ref_deltas

def test_expect_ref_deltas():
    values = [True]

    with expect_ref_deltas(values, delta=0):
        pass

    l = []
    with expect_ref_deltas(values, delta=1):
        l.append(True)


def test_expect_ref_deltas_ints():
    values = [201, 220]

    with expect_ref_deltas(values, delta=0):
        pass

    l = []
    with expect_ref_deltas(values, delta=1):
        l.append(201)
        l.append(220)