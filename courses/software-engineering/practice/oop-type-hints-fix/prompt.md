# Add type hints and fix the bugs they reveal

The starter is a small module about people's ages. It has no type hints and three bugs. Each bug is the kind a type checker (mypy or pyright) points out as soon as the hints are there: a value that might be `None` used as if it were an `int`, and an `int` glued onto a `str`.

Add these exact annotations, then fix the code so it behaves as described:

```python
def find_age(ages: dict[str, int], name: str) -> int | None: ...
def total_age(ages: dict[str, int], names: list[str]) -> int: ...
def describe(name: str, age: int | None) -> str: ...
def apply_all(values: list[int], fn: Callable[[int], int]) -> list[int]: ...
```

- `ages` maps a person's name to their age, for example `{"Ada": 36, "Alan": 41}`.
- `find_age(ages, name)` returns the age, or `None` if the name isn't there. (The starter crashes with `KeyError` instead.)
- `total_age(ages, names)` adds up the ages of the given names and **skips** names that aren't in `ages`. (The starter crashes when `find_age` gives back `None`.)
- `describe(name, age)` returns `"Ada is 36"`, or `"Ada's age is unknown"` when `age` is `None`. (The starter crashes trying `str + int`.)
- `apply_all(values, fn)` returns `[fn(v) for v in values]`. `Callable` comes from `collections.abc` (or `typing`).

The tests check the behaviour and also read your annotations with `typing.get_type_hints`, so spell them exactly as above.

## Example

```python
ages = {"Ada": 36, "Alan": 41}
find_age(ages, "Grace")                  # None
total_age(ages, ["Ada", "Grace", "Alan"]) # 77
describe("Ada", 36)                      # "Ada is 36"
apply_all([1, 2], lambda n: n * 10)      # [10, 20]
```
