# Return, don't print

The starter code has two functions that *look* like they work: Run it and you see the right numbers. But they `print` their answers instead of `return`ing them, so any code that calls them gets `None` back. Fix them.

```python
def average(numbers: list[float]) -> float | None: ...
def format_price(amount: float) -> str: ...
```

- `average(numbers)` returns the mean (the sum divided by how many there are). For an empty list, return `None` instead of crashing with a division by zero.
- `format_price(amount)` returns the amount as dollars with exactly two decimal places, e.g. `3.5` → `"$3.50"`.

Neither function should print anything.

## Example

```python
average([1, 2, 3, 4])   # 2.5
average([])             # None
format_price(3.5)       # "$3.50"
total = format_price(average([2, 4]))   # "$3.00"   (only works once both return)
```
