MAX_QUALITY = 50


class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return f"Item({self.name!r}, {self.sell_in}, {self.quality})"


def daily_quality_change(name: str, expired: bool) -> int:
    """How much quality changes today for this kind of item."""
    rate = 2 if expired else 1
    if name == "Aged Cheese":
        return rate
    if name == "Fresh Bread":
        return -2 * rate
    return -rate


def update_inventory(items: list[Item]) -> None:
    for item in items:
        if item.name == "Honey":
            continue
        item.sell_in -= 1
        change = daily_quality_change(item.name, expired=item.sell_in < 0)
        item.quality = max(0, min(MAX_QUALITY, item.quality + change))


if __name__ == "__main__":
    items = [Item("Croissant", 1, 10), Item("Fresh Bread", 0, 5), Item("Aged Cheese", 3, 49)]
    update_inventory(items)
    print(items)
