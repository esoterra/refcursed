# Refcursed

Refcursed is a library for the things you can, but should not, do with the ability to determine the number of current references to any object.
At import time, the library emits a warning because really what are you doing.

# Use Cases

## Bringing balance to the universe

Did you know that the Python runtime knows how many references to `True` and `False` exist at any given time?

Have you ever wanted to bring balance to your programs and know that they're just as `True` as they are `False`?

Look no further! Refcursed provides one simple function you can call to right the universe.

```py
import refcursed
refcursed.balance_bool()
```

## Unit testing

Have you ever wanted to make sure that your code you're calling isn't creating extra aliases to a certain value?

Now you can! With the new `expect_ref_delta` context manager (compare to `pytest.raises`), you can right unit tests that ensure exactly the amount of references you expect to be added/removed are.

```py
from refcursed import expect_ref_delta

my_list = []
with expect_ref_delta(201, delta=2):
    my_list.append(201)
    my_list.append(201)
```

If you want to check multiple at the same time, we even have a pluralized version.
```py
from refcursed import expect_ref_deltas

my_list = []
with expect_ref_deltas([201, 220], delta=1):
    my_list.append(201)
    my_list.append(220)
```

## Counting sort but ~~better~~ worse

The thing about counting sort is that you have to have counters for your different values. This is really silly though, because the runtime has counters for all of them anyway, the refcount. Our state of the art counting sort implementation uses those counters instead of its own for... performance?

```py
import refcursed
result = refcursed.refcounting_sort([4, 4, 4, 3, 2, 1, 1])
assert result = [1, 1, 2, 3, 4, 4, 4]
```

## Counting values

The same mechanism that lets us perform counting sort, taking refcounts before and after deleting things, allows us to count arbitrary lists contents as well.

```py
import refcursed
result = refcursed.count_values([4, 4, 4, 3, 2, 1, 1])
assert result == {
    1: 2,
    2: 1,
    3: 1,
    4: 3
}
```

## Comparing and Sorting by refcount

The library also provides utilities for comparing the refcounts of two values and sorting sequences of values by refcount.

```py
import refcursed
assert refcursed.sort_refcount([1, 2, 3]) == ... # varies
assert refcursed.compare_refcounts(1, 2) == ... #varies
```

See the [Integers](#integers) section to find out why these are subtly non-trivial.


# Considerations, Caveats, and Curiosities

Most of the characteristics of `sys.getrefcount` are intuitive and you might guess, but others you may not.

## `str` Interning

Strings in Python sometimes act as separate objects that don't `is` compare true and don't have the same refcount, but some are the same and do. The latter case is due to interning, where Python stores one `str` object for multiple (potentially independent) instances of the same string value.

Interning sometimes happens automatically, like in all string literals, and can also be done manual, using `sys.intern`. Be aware of when interning is/isn't happening and how that may affect the behavior of refcounting.

## `int` and `bool` Interning

Similarly to strings, integers and boolean values are also interned but following different rules. Any time an integer (within some size limit) is returned by an arithmetic operation, Python pulls the correct integer object from a table instead of creating a new one incrementing the count for that integer. Booleans work much the same way but are always interned because there are only two possible values.

One fun quirk of this is that the integers returned by `sys.getrefcount` can be interned and increment the refcount for that integer. Under very specific circumstances this can change the outcome of a comparison.

```py
# If B is equal to the integer that is the refcount of A
# and B is a small enough integer to be automatically interned
# and the refcount of B is one less than the refcount of A,
# then even though A had a larger refcount the act of observing them
# has made them equal and this condition will fail.
assert sys.getrefcount(A) > sys.getrefcount(B)
```

This may sound very precise and very unlikely, but it really isn't.
It can easily occur whenever sorting or comparing small integer values by refcount.
For robustness, all comparisons in the refcursed library either use `float(sys.getrefcount(...))` to store refcounts without modifying others or compensate for the case above.
