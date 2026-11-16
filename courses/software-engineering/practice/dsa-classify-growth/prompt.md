# Guess the Big-O from measurements

You ran some code at several input sizes and counted the steps. Now write a function that looks at those numbers and names the growth rate.

```python
def classify_growth(sizes: list[int], step_counts: list[int]) -> str: ...
```

- `sizes`: the input sizes you tried, smallest first, all bigger than 1. Example: `[1000, 2000, 4000, 8000]`.
- `step_counts`: how many steps the code took at each size (same order, same length).
- Return one of: `"O(1)"`, `"O(log n)"`, `"O(n)"`, `"O(n log n)"`, `"O(n^2)"`.

**The method: the ratio test.** For each candidate growth function `f`:

```
f(n) = 1          for O(1)
f(n) = log2(n)    for O(log n)
f(n) = n          for O(n)
f(n) = n·log2(n)  for O(n log n)
f(n) = n²         for O(n^2)
```

divide every step count by `f(size)`. If `f` is the right shape, those ratios are all about the same number (the hidden constant). Measure how "flat" they are with `max(ratios) / min(ratios)` and return the candidate whose value is **closest to 1**. Use `math.log2`.

## Example

```python
classify_growth([1000, 2000, 4000, 8000], [3005, 6005, 12005, 24005])   # "O(n)"
classify_growth([1000, 2000, 4000, 8000], [1_000_000, 4_000_000, 16_000_000, 64_000_000])  # "O(n^2)"
classify_growth([1000, 2000, 4000, 8000], [7, 7, 7, 7])                 # "O(1)"
```

In the first example the ratios for `f(n) = n` are about `3.005, 3.0025, 3.001, 3.0006`: almost flat. The `+5` and the `3×` don't change the answer, which is exactly why Big-O drops constants.
