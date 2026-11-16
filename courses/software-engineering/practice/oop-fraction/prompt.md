# A Fraction class that behaves like a number

Python's `+`, `==` and the way objects print are all powered by **special methods** (also called "dunder" methods, for the double underscores). Write a `Fraction` class that uses them.

```python
class Fraction:
    def __init__(self, numerator: int, denominator: int): ...
    def __add__(self, other: "Fraction") -> "Fraction": ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
```

- `numerator` is the top number, `denominator` the bottom one. Store them as the attributes `numerator` and `denominator`.
- Always store the fraction **reduced**: divide both numbers by their greatest common divisor (`math.gcd`). `Fraction(2, 4)` is stored as `1/2`.
- Keep the sign on the numerator: the denominator is always positive. `Fraction(1, -2)` is stored as `-1/2`.
- A denominator of `0` raises `ZeroDivisionError`.
- `a + b` returns a **new** `Fraction`: `a/b + c/d = (a·d + c·b) / (b·d)`, reduced.
- `==` compares the reduced values, so `Fraction(1, 2) == Fraction(2, 4)` is `True`. If `other` isn't a `Fraction`, return `NotImplemented`.
- `repr(Fraction(1, 2))` returns `Fraction(1, 2)`.

## Example

```python
Fraction(2, 4)                     # Fraction(1, 2)
Fraction(1, 2) + Fraction(1, 3)    # Fraction(5, 6)
Fraction(1, -2)                    # Fraction(-1, 2)
Fraction(1, 2) == Fraction(3, 6)   # True
Fraction(0, 5)                     # Fraction(0, 1)
```
