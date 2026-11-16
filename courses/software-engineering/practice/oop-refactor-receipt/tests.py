import contextlib
import io
from unittest.mock import patch

import solution

ITEMS = [
    {"name": "Coffee", "price_cents": 350, "qty": 2},
    {"name": "Bagel", "price_cents": 250, "qty": 1},
    {"name": "Muffin", "price_cents": 300, "qty": 0},
]


def run_process(order):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        total = solution.process(order)
    return total, out.getvalue()


def test_process_output_is_unchanged():
    cases = [
        ({"items": ITEMS, "code": "SAVE10"}, 855, "Coffee x2  7.00\nBagel x1  2.50\nSubtotal  9.50\nDiscount  -0.95\nTotal  8.55\n"),
        ({"items": ITEMS}, 950, "Coffee x2  7.00\nBagel x1  2.50\nSubtotal  9.50\nTotal  9.50\n"),
        ({"items": ITEMS[1:2], "code": "FLAT5"}, 0, "Bagel x1  2.50\nSubtotal  2.50\nDiscount  -2.50\nTotal  0.00\n"),
    ]
    for order, want_total, want_text in cases:
        got = run_process(order)
        assert got == (want_total, want_text), f"expected {(want_total, want_text)!r}, got {got!r}"


def test_calculate_subtotal_ignores_zero_quantity():
    got = solution.calculate_subtotal(ITEMS)
    assert got == 950, f"expected 950, got {got!r}"
    assert solution.calculate_subtotal([]) == 0, "no items should give a subtotal of 0"


def test_apply_discount_handles_every_code():
    cases = [(950, "SAVE10", 855), (999, "SAVE10", 900), (2000, "FLAT5", 1500), (300, "FLAT5", 0), (950, "BOGUS", 950), (950, None, 950)]
    for subtotal, code, want in cases:
        got = solution.apply_discount(subtotal, code)
        assert got == want, f"apply_discount({subtotal}, {code!r}): expected {want!r}, got {got!r}"


def test_format_receipt_returns_text():
    got = solution.format_receipt(ITEMS, 950, 855)
    want = "Coffee x2  7.00\nBagel x1  2.50\nSubtotal  9.50\nDiscount  -0.95\nTotal  8.55"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_helpers_never_print():
    with patch("builtins.print") as fake_print:
        solution.calculate_subtotal(ITEMS)
        solution.apply_discount(950, "SAVE10")
        solution.format_receipt(ITEMS, 950, 855)
    assert fake_print.call_count == 0, f"helpers should return values, not print (print was called {fake_print.call_count} times)"
