# FizzBuzz

A classic first interview warm-up. It checks that you can combine a loop with conditions in the right order.

```python
def fizzbuzz(n: int) -> list[str]: ...
```

- `n` is how far to count, starting at 1.
- Return a list of `n` strings, one for each number from 1 to `n`:
  - `"FizzBuzz"` if the number is divisible by both 3 and 5,
  - `"Fizz"` if it's divisible by 3 only,
  - `"Buzz"` if it's divisible by 5 only,
  - otherwise the number itself as a string, e.g. `"7"`.
- `n` of 0 returns an empty list.

**Order matters:** if you check "divisible by 3" first, 15 becomes `"Fizz"` and never reaches `"FizzBuzz"`.

## Example

```python
fizzbuzz(5)    # ["1", "2", "Fizz", "4", "Buzz"]
fizzbuzz(15)[-1]   # "FizzBuzz"
```
