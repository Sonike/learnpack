# Sum the digits, count the vowels

Two warm-ups for the **accumulator** pattern: start a total at zero, then add to it inside a loop.

```python
def sum_of_digits(n: int) -> int: ...
def count_vowels(s: str) -> int: ...
```

- `sum_of_digits(n)` returns the sum of the digits of the whole number `n`. Treat a negative number like a positive one (`abs(n)`). Do it with arithmetic: `n % 10` is the last digit and `n // 10` removes it.
- `count_vowels(s)` returns how many letters in `s` are vowels (`a e i o u`), upper or lower case.

## Example

```python
sum_of_digits(1234)    # 10
sum_of_digits(-505)    # 10
count_vowels("Hello World")   # 3
count_vowels("rhythm")        # 0
```
