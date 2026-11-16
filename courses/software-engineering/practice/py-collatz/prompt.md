# Collatz steps

Pick a whole number. If it's even, halve it. If it's odd, multiply by 3 and add 1. Repeat. Every starting number anyone has ever tried eventually reaches 1, but nobody has proved it always will. You don't know in advance how many steps it takes, so this is a job for a `while` loop.

```python
def collatz_steps(n: int) -> int: ...
```

- `n` is a whole number, 1 or more.
- Return how many steps it takes to reach 1. Starting at 1 takes 0 steps.

## Example

```python
collatz_steps(1)   # 0
collatz_steps(6)   # 8    6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
collatz_steps(27)  # 111
```

**Careful:** the loop must change `n` every time round, or it never ends. If your Run hangs, stop it and check that line.
