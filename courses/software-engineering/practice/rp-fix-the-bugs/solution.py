def stock_level(stock: dict[str, int], item: str) -> int:
    """How many of item are in stock. Items missing from the dict count as 0."""
    return stock.get(item, 0)


def order_summary(name: str, quantity: int) -> str:
    """A sentence like "Ada ordered 3 items" ("item" when quantity is 1)."""
    word = "item" if quantity == 1 else "items"
    return f"{name} ordered {quantity} {word}"


def price_changes(prices: list[float]) -> list[float]:
    """The change from each price to the next: [10, 12.5, 11] -> [2.5, -1.5]."""
    changes = []
    for i in range(len(prices) - 1):
        changes.append(prices[i + 1] - prices[i])
    return changes
