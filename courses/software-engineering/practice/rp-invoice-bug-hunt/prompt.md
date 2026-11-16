# Bug hunt: the invoice total

A colleague wrote `invoice_total` and the numbers on customers' invoices are wrong. There are **three bugs** in the starter. Your job is to find and fix all three, without rewriting the code from scratch.

Work like the lesson describes: run the tests, pick one failing test, form a hypothesis, check it (with `print`, or a breakpoint in VS Code if you have the code locally), fix, re-run. One bug at a time.

## What the code should do

```python
def invoice_total(lines: list[dict], discounts: dict[str, float]) -> float:
```

- `lines` is a list of invoice lines like `{"sku": "pen", "price": 2.50, "qty": 4}`. `sku` is the product code, `price` the price of one unit, `qty` how many.
- `discounts` maps a sku to a percentage off (`25` means 25% off that line). Skus not in the dict have no discount.
- Lines with a `qty` of 0 or less are ignored.
- **Shipping:** an order whose discounted subtotal is **100.00 or more** ships free. Otherwise shipping costs 5.00. An empty order (subtotal 0) has no shipping.
- Return subtotal + shipping, rounded to 2 decimals.

## Examples

```python
invoice_total([{"sku": "pen", "price": 2.50, "qty": 4}], {})            # 15.0  (10.00 + 5.00 shipping)
invoice_total([{"sku": "book", "price": 40.0, "qty": 2}], {"book": 25})  # 65.0  (80.00 - 25% = 60.00, + 5.00)
invoice_total([{"sku": "mug", "price": 50.0, "qty": 2}], {})            # 100.0 (free shipping)
invoice_total([], {})                                                  # 0.0
```

> **Tip:** the three bugs are independent. Fixing one may make *more* tests pass without making all of them pass. That's normal: keep going.
