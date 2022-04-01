from refcursed import count_values

def test_count_values():
    counts = count_values(['a', 'a', 'b', 'b', 'b', 'c', 'd' ,'d'])
    assert counts == {
        'a': 2,
        'b': 3,
        'c': 1,
        'd': 2
    }

def test_count_values_ints():
    counts = count_values([1, 1, 2, 2, 2, 3, 4, 4])
    assert counts == {
        1: 2,
        2: 3,
        3: 1,
        4: 2
    }
