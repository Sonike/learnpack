# Split the bill

A group has dinner. Work out what each person pays, tip included.

```python
def split_bill(total: float, people: int, tip_percent: float) -> float: ...
```

- `total`: the bill before the tip, e.g. `120.0`.
- `people`: how many people share it (1 or more).
- `tip_percent`: the tip as a percentage, e.g. `15` for 15%. `0` means no tip.
- Return each person's share, **rounded to cents** (2 decimal places) with `round(x, 2)`.

Steps: the tip is `total * tip_percent / 100`; add it to the total; divide by `people`; round **once, at the end**. Rounding early (for example rounding the tip first) can be a cent off.

## Example

```python
split_bill(100, 4, 0)      # 25.0
split_bill(100, 3, 0)      # 33.33
split_bill(120, 4, 15)     # 34.5
```
