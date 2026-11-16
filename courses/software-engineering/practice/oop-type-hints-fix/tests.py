import collections.abc
import typing

from solution import apply_all, describe, find_age, total_age

AGES = {"Ada": 36, "Alan": 41}


def test_find_age_returns_none_for_missing_name():
    assert find_age(AGES, "Ada") == 36, f"expected 36, got {find_age(AGES, 'Ada')!r}"
    got = find_age(AGES, "Grace")
    assert got is None, f"expected None, got {got!r}"


def test_total_age_skips_missing_names():
    got = total_age(AGES, ["Ada", "Grace", "Alan"])
    assert got == 77, f"expected 77, got {got!r}"
    assert total_age(AGES, []) == 0, "no names should total 0"


def test_describe_handles_known_and_unknown_age():
    for args, want in [(("Ada", 36), "Ada is 36"), (("Ada", None), "Ada's age is unknown")]:
        got = describe(*args)
        assert got == want, f"expected {want!r}, got {got!r}"


def test_apply_all_maps_every_value():
    got = apply_all([1, 2, 3], lambda n: n * 10)
    assert got == [10, 20, 30], f"expected [10, 20, 30], got {got!r}"


def test_hints_match_the_signatures():
    expected = {
        find_age: {"ages": dict[str, int], "name": str, "return": int | None},
        total_age: {"ages": dict[str, int], "names": list[str], "return": int},
        describe: {"name": str, "age": int | None, "return": str},
    }
    for fn, want in expected.items():
        got = typing.get_type_hints(fn)
        assert got == want, f"{fn.__name__}: expected hints {want!r}, got {got!r}"


def test_apply_all_hints_use_callable():
    hints = typing.get_type_hints(apply_all)
    assert hints.get("values") == list[int], f"values: expected list[int], got {hints.get('values')!r}"
    assert hints.get("return") == list[int], f"return: expected list[int], got {hints.get('return')!r}"
    fn = hints.get("fn")
    got = (typing.get_origin(fn), typing.get_args(fn))
    want = (collections.abc.Callable, ([int], int))
    assert got == want, f"fn: expected Callable[[int], int], got {fn!r}"
