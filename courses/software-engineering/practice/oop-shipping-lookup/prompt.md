# Replace a long if/elif with a lookup table

`shipping_cost` in the starter is a seven-branch `if/elif` chain. Every branch does the same calculation with different numbers. That's a smell: the *data* (the rates) is tangled up with the *logic* (the formula). Adding a zone means copying a branch, and a typo in one branch is easy to miss.

Refactor it so the rates live in data:

```python
@dataclass(frozen=True)
class Rate:
    base_cents: int
    per_kg_cents: int

RATES: dict[str, Rate] = {...}   # one entry per zone

def shipping_cost(zone: str, weight_g: int) -> int: ...
```

- `zone` is the destination, such as `"local"` or `"europe"`. `weight_g` is the parcel weight in grams.
- The cost is `base_cents + per_kg_cents × (kilograms, rounded up)`. A 1-gram parcel counts as 1 kg; 1001 g counts as 2 kg.
- An unknown zone raises `ValueError`. A weight of 0 or less raises `ValueError`.
- `shipping_cost` must look the zone up in `RATES` instead of using `if/elif`. The tests check this by adding a new zone to `RATES` and expecting `shipping_cost` to handle it.

Keep every price exactly as it is today: the hidden tests are the same behaviour tests that passed on the old version, plus the lookup check.

> **Tip:** the integer trick for "divide and round up" is `-(-weight_g // 1000)`. `math.ceil(weight_g / 1000)` works too.

## Example

```python
shipping_cost("local", 500)      # 350   (300 + 50 × 1)
shipping_cost("europe", 2500)    # 2050  (1300 + 250 × 3)
shipping_cost("mars", 100)       # ValueError: unknown zone
```
