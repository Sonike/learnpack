from solution import Item, update_inventory


def after_days(name, sell_in, quality, days=1):
    item = Item(name, sell_in, quality)
    for _ in range(days):
        update_inventory([item])
    return (item.sell_in, item.quality)


def test_normal_item_loses_one_quality_a_day():
    got = after_days("Croissant", 5, 10)
    assert got == (4, 9), f"expected (4, 9), got {got!r}"


def test_normal_item_past_its_date_loses_two():
    got = after_days("Croissant", 0, 10)
    assert got == (-1, 8), f"expected (-1, 8), got {got!r}"
    got = after_days("Croissant", 0, 1)
    assert got == (-1, 0), f"quality should never go below 0, got {got!r}"


def test_aged_cheese_improves_but_caps_at_50():
    for args, want in [(("Aged Cheese", 5, 10), (4, 11)), (("Aged Cheese", 0, 10), (-1, 12)), (("Aged Cheese", 0, 49), (-1, 50)), (("Aged Cheese", 5, 50), (4, 50))]:
        got = after_days(*args)
        assert got == want, f"{args}: expected {want!r}, got {got!r}"


def test_honey_never_changes():
    got = after_days("Honey", 5, 30, days=10)
    assert got == (5, 30), f"expected (5, 30), got {got!r}"


def test_fresh_bread_goes_stale_twice_as_fast():
    for args, want in [(("Fresh Bread", 3, 10), (2, 8)), (("Fresh Bread", 0, 10), (-1, 6)), (("Fresh Bread", 0, 3), (-1, 0))]:
        got = after_days(*args)
        assert got == want, f"{args}: expected {want!r}, got {got!r}"


def test_updates_a_mixed_list_in_place():
    items = [Item("Croissant", 1, 10), Item("Fresh Bread", 0, 5), Item("Aged Cheese", 3, 49)]
    update_inventory(items)
    got = [(i.sell_in, i.quality) for i in items]
    assert got == [(0, 9), (-1, 1), (2, 50)], f"expected [(0, 9), (-1, 1), (2, 50)], got {got!r}"
