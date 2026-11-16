# Money that can't be mixed up

A price of `12.50` means nothing without a currency, and adding dollars to euros is a bug. Write a **frozen** dataclass that makes those mistakes impossible.

```python
@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str

    def __add__(self, other: "Money") -> "Money": ...
    def __str__(self) -> str: ...
```

- `amount_cents` is a whole number of cents (`1250` means 12.50). `currency` is a three-letter code like `"USD"`.
- `frozen=True` means fields can't be changed after creation: `price.amount_cents = 0` raises `dataclasses.FrozenInstanceError`. To "change" money you create a new `Money`.
- `a + b` returns a new `Money` with the amounts added. If the currencies differ, raise `ValueError`.
- `str(Money(1250, "USD"))` returns `"12.50 USD"`. Always two decimal places. Negative amounts show a minus sign: `Money(-250, "EUR")` → `"-2.50 EUR"`.
- Because it's a frozen dataclass, `==` and `hash()` already work. Two `Money` values with the same amount and currency are equal.

## Example

```python
price = Money(1250, "USD")
tax = Money(100, "USD")
str(price + tax)                  # "13.50 USD"
price + Money(500, "EUR")         # ValueError: cannot add USD and EUR
Money(5, "USD")                   # str → "0.05 USD"
```
