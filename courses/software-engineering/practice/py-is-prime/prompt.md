# Is it prime?

A **prime** is a whole number greater than 1 whose only divisors are 1 and itself: 2, 3, 5, 7, 11, …

```python
def is_prime(n: int) -> bool: ...
```

- `n` is any whole number (it may be 0, 1 or negative; those are not prime).
- Return `True` if `n` is prime.

**Make it fast.** You don't need to try every number below `n`. If `n = a × b`, one of `a` or `b` is at most √n. So you only need to try divisors `d` while `d * d <= n`. For `n = 1,000,000,007` that's about 31,600 checks instead of a billion. The tests include a big prime, so the slow version will time out.

**Watch the edge:** use `<=`, not `<`. With `<`, 49 (= 7 × 7) would look prime.

## Example

```python
is_prime(2)    # True
is_prime(1)    # False
is_prime(49)   # False
is_prime(97)   # True
```
