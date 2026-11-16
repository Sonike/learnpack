from solution import invoice_total


def pen(qty=4):
    return {"sku": "pen", "price": 2.50, "qty": qty}


def test_one_line_without_a_discount():
    got = invoice_total([pen()], {})
    assert got == 15.0, f"expected 15.0 (10.00 + 5.00 shipping), got {got!r}"


def test_discount_takes_a_percentage_off():
    got = invoice_total([{"sku": "book", "price": 40.0, "qty": 2}], {"book": 25})
    assert got == 65.0, f"expected 65.0 (80.00 - 25% = 60.00, + 5.00), got {got!r}"


def test_every_line_is_counted():
    lines = [pen(), {"sku": "book", "price": 40.0, "qty": 2}]
    got = invoice_total(lines, {"book": 25})
    assert got == 75.0, f"expected 75.0 (10.00 + 60.00 + 5.00), got {got!r}"


def test_exactly_100_ships_free():
    got = invoice_total([{"sku": "mug", "price": 50.0, "qty": 2}], {})
    assert got == 100.0, f"expected 100.0 (free shipping from 100.00), got {got!r}"


def test_zero_quantity_lines_are_ignored():
    got = invoice_total([pen(qty=0), pen(qty=2)], {})
    assert got == 10.0, f"expected 10.0 (5.00 + 5.00 shipping), got {got!r}"


def test_empty_invoice_is_zero():
    got = invoice_total([], {})
    assert got == 0.0, f"expected 0.0, got {got!r}"
