from refcursed import sort_refcount, expect_ref_deltas


def test_sort_refcount_wont_add_refs():
    data1 = [10, 12, 9, 6, 4, 7, 5, 18, 3, 15, 2, 14, 10, 1, 18, 10, 6, 5, 15, 11]
    unique = list(sorted(set(data1)))

    with expect_ref_deltas(unique, delta=0):
        data1_sorted = sort_refcount(data1)
        data1.clear()

    del data1_sorted

def test_sort_refcount_wont_add_refs():
    data1 = []
    for _ in range(100):
        data1.append(10)
    for _ in range(200):
        data1.append(9)
    for _ in range(300):
        data1.append(8)
    for _ in range(400):
        data1.append(7)
    for _ in range(500):
        data1.append(6)

    data1_sorted = sort_refcount(data1)

    assert data1_sorted == sorted(data1_sorted)

