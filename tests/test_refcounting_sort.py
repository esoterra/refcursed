from refcursed import refcounting_sort

def test_refcounting_sort():
    result = refcounting_sort([4, 4, 4, 3, 2, 1, 1])
    print(result)
    assert result == [1, 1, 2, 3, 4, 4, 4]