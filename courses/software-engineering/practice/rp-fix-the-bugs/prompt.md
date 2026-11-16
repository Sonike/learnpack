# Fix three classic bugs

The starter holds three small functions from a shop's code. Each one crashes with one of the most common Python exceptions. Run the starter, read each traceback bottom-up, and fix the function so it does what its docstring says. Don't rewrite them from scratch: each fix is one or two lines.

```python
def stock_level(stock: dict[str, int], item: str) -> int:
def order_summary(name: str, quantity: int) -> str:
def price_changes(prices: list[float]) -> list[float]:
```

1. **`stock_level`** returns how many of `item` are in `stock` (a dict mapping item name to count). An item that isn't in the dict has a stock level of `0`. Right now it raises `KeyError`.
2. **`order_summary`** returns a sentence like `"Ada ordered 3 items"` (use `"item"`, singular, when `quantity` is 1). Right now it raises `TypeError`.
3. **`price_changes`** returns the change between each price and the next one. Right now it raises `IndexError`.

## Examples

```python
stock_level({"apple": 4}, "apple")     # 4
stock_level({"apple": 4}, "pear")      # 0
order_summary("Ada", 3)                # "Ada ordered 3 items"
order_summary("Grace", 1)              # "Grace ordered 1 item"
price_changes([10.0, 12.5, 11.0])      # [2.5, -1.5]
price_changes([10.0])                  # []
```
