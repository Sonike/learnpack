class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return f"Item({self.name!r}, {self.sell_in}, {self.quality})"


def update_inventory(items: list[Item]) -> None:
    for item in items:
        if item.name != "Aged Cheese":
            if item.quality > 0:
                if item.name != "Honey":
                    item.quality = item.quality - 1
        else:
            if item.quality < 50:
                item.quality = item.quality + 1
        if item.name != "Honey":
            item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            if item.name != "Aged Cheese":
                if item.quality > 0:
                    if item.name != "Honey":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
    # TODO: "Fresh Bread" loses 2 quality a day, 4 once past its date


if __name__ == "__main__":
    # Characterization tests: record today's behaviour before you change anything.
    croissant = Item("Croissant", 1, 10)
    update_inventory([croissant])
    assert (croissant.sell_in, croissant.quality) == (0, 9), croissant
    # TODO: add asserts for a past-date item, Aged Cheese near 50, and Honey

    items = [Item("Croissant", 1, 10), Item("Fresh Bread", 0, 5), Item("Aged Cheese", 3, 49), Item("Honey", 5, 30)]
    update_inventory(items)
    print(items)
