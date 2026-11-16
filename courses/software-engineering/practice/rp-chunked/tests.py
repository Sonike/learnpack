import itertools
import types

from solution import chunked


def test_splits_into_equal_chunks_and_a_shorter_last_one():
    got = list(chunked([1, 2, 3, 4, 5], 2))
    want = [[1, 2], [3, 4], [5]]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_works_on_any_iterable():
    got = list(chunked("abcdef", 3))
    want = [["a", "b", "c"], ["d", "e", "f"]]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_empty_input_yields_nothing():
    got = list(chunked([], 4))
    assert got == [], f"expected [], got {got!r}"


def test_is_a_generator_that_handles_endless_input():
    gen = chunked(itertools.count(), 3)
    assert isinstance(gen, types.GeneratorType), "chunked should be a generator function (use yield)"
    got = list(itertools.islice(gen, 2))
    want = [[0, 1, 2], [3, 4, 5]]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_only_pulls_the_items_it_needs():
    pulled = []

    def source():
        for n in range(100):
            pulled.append(n)
            yield n

    first = next(chunked(source(), 4))
    assert first == [0, 1, 2, 3], f"expected [0, 1, 2, 3], got {first!r}"
    assert len(pulled) == 4, f"the first chunk should pull 4 items, but {len(pulled)} were pulled"


def test_rejects_a_size_below_one():
    try:
        next(chunked([1, 2], 0))
    except ValueError:
        return
    assert False, "expected ValueError for size 0"
