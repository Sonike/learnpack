# Refactor a messy function into pure helpers

The starter has `process(d)`: it works, but it is one long function with deep nesting, one-letter names, a magic number and printing mixed into the maths. Your job is to **refactor** it: change its structure without changing what it does.

Split it into three **pure** helpers (they return values and never `print`) and keep `process` as a thin function that wires them together and does the printing:

```python
def calculate_subtotal(items: list[dict]) -> int: ...
def apply_discount(subtotal: int, code: str | None) -> int: ...
def format_receipt(items: list[dict], subtotal: int, total: int) -> str: ...
def process(order: dict) -> int: ...
```

What the code does today (keep all of it):

- An `order` is a dict like `{"items": [...], "code": "SAVE10"}`. `"code"` may be missing or `None`.
- Each item is `{"name": "Coffee", "price_cents": 350, "qty": 2}`. Items with `qty` of 0 or less are ignored everywhere.
- **`calculate_subtotal(items)`** returns the sum of `price_cents * qty`, in cents.
- **`apply_discount(subtotal, code)`** returns the **total after the discount**:
  - `"SAVE10"` takes off 10%, rounded down to a whole cent (`subtotal * 10 // 100`);
  - `"FLAT5"` takes off 500 cents, but never more than the subtotal;
  - any other code, or no code, takes off nothing.
- **`format_receipt(items, subtotal, total)`** returns the receipt as one string, lines joined with `"\n"`:

  ```
  Coffee x2  7.00
  Bagel x1  2.50
  Subtotal  9.50
  Discount  -0.95
  Total  8.55
  ```

  Amounts always have two decimals. The `Discount` line appears only when the discount (`subtotal - total`) is more than 0.
- **`process(order)`** prints that receipt and returns the total in cents.

The hidden tests check that `process` prints exactly what it printed before, that each helper gives the right answer, and that the helpers never call `print`.

> **Tip:** before you change anything, Run the starter and save its output. That's your "before" picture. After each small change, Run again and compare.
