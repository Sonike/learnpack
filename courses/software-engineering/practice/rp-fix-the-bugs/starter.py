def stock_level(stock: dict[str, int], item: str) -> int:
    """How many of item are in stock. Items missing from the dict count as 0."""
    return stock[item]


def order_summary(name: str, quantity: int) -> str:
    """A sentence like "Ada ordered 3 items" ("item" when quantity is 1)."""
    word = "item" if quantity == 1 else "items"
    return name + " ordered " + quantity + " " + word


def price_changes(prices: list[float]) -> list[float]:
    """The change from each price to the next: [10, 12.5, 11] -> [2.5, -1.5]."""
    changes = []
    for i in range(len(prices)):
        changes.append(prices[i + 1] - prices[i])
    return changes


if __name__ == "__main__":
    import traceback

    # Each call is wrapped so you see every traceback, not just the first one.
    for call in (
        lambda: stock_level({"apple": 4}, "pear"),
        lambda: order_summary("Ada", 3),
        lambda: price_changes([10.0, 12.5, 11.0]),
    ):
        try:
            print(call())
        except Exception:
            traceback.print_exc()
            print()
