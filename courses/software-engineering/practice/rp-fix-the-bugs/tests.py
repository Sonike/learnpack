from solution import order_summary, price_changes, stock_level


def test_stock_level_for_a_known_item():
    got = stock_level({"apple": 4, "pear": 0}, "apple")
    assert got == 4, f"expected 4, got {got!r}"


def test_stock_level_of_a_missing_item_is_zero():
    got = stock_level({"apple": 4}, "banana")
    assert got == 0, f"expected 0, got {got!r}"


def test_order_summary_uses_plural_items():
    got = order_summary("Ada", 3)
    want = "Ada ordered 3 items"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_order_summary_uses_singular_for_one():
    got = order_summary("Grace", 1)
    want = "Grace ordered 1 item"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_price_changes_between_neighbours():
    got = price_changes([10.0, 12.5, 11.0])
    want = [2.5, -1.5]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_price_changes_of_one_or_no_prices_is_empty():
    assert price_changes([10.0]) == [], f"expected [], got {price_changes([10.0])!r}"
    assert price_changes([]) == [], f"expected [], got {price_changes([])!r}"
