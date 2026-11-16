# TODO: add the type hints from the prompt to all four functions, then fix the three bugs.
from collections.abc import Callable


def find_age(ages, name):
    return ages[name]  # bug: crashes on a missing name instead of returning None


def total_age(ages, names):
    total = 0
    for name in names:
        total += find_age(ages, name)  # bug: find_age can return None
    return total


def describe(name, age):
    return name + " is " + age  # bug: can't add an int to a str, and age can be None


def apply_all(values, fn):
    return [fn(v) for v in values]


if __name__ == "__main__":
    ages = {"Ada": 36, "Alan": 41}
    for call in (lambda: find_age(ages, "Grace"), lambda: total_age(ages, ["Ada", "Grace", "Alan"]), lambda: describe("Ada", 36)):
        try:
            print(call())
        except Exception as e:
            print(type(e).__name__, e)
    print(apply_all([1, 2], lambda n: n * 10))
