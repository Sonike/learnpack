# Write tests that catch bugs

This time **you** write the tests. Write a function `check_is_leap_year(fn)` that tests someone else's leap-year function with `assert` statements.

```python
def check_is_leap_year(fn) -> None: ...
```

- `fn` is a function that takes a year (`int`) and returns `True` if it's a leap year, `False` if not.
- Your checker calls `fn` with years you choose and `assert`s the answers. If `fn` is correct, your checker finishes quietly (returns `None`). If `fn` is wrong, one of your asserts fails and raises `AssertionError`.

The leap-year rule (the Gregorian calendar):

- A year divisible by 4 is a leap year (2024),
- **except** a year divisible by 100 is not (1900),
- **except** a year divisible by 400 is (2000).

The hidden tests hand your checker one correct implementation, which must pass, and **five buggy ones**, each of which your checker must catch. Each bug gets one part of the rule wrong. To catch them all, you need a year for every part of the rule. Think: which years would tell a correct function apart from one that only checks `% 4`?

Give each assert a message so a failure explains itself:

```python
assert fn(2024) is True, "2024 is divisible by 4, so it is a leap year"
```

## Example

```python
def correct(year): ...
def only_checks_4(year): return year % 4 == 0

check_is_leap_year(correct)        # passes quietly
check_is_leap_year(only_checks_4)  # AssertionError: 1900 is divisible by 100 ...
```
