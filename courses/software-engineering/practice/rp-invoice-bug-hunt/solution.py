FREE_SHIPPING_FROM = 100.00
SHIPPING_FEE = 5.00


def line_total(line: dict, discounts: dict[str, float]) -> float:
    """price * qty, minus the line's discount (a percentage) if its sku has one."""
    subtotal = line["price"] * line["qty"]
    percent = discounts.get(line["sku"], 0)
    return subtotal * (1 - percent / 100)  # fix 1: keep what's left after the discount


def shipping(subtotal: float) -> float:
    """Free from 100.00 upwards, otherwise 5.00. An empty order has no shipping."""
    if subtotal == 0:
        return 0.0
    if subtotal >= FREE_SHIPPING_FROM:  # fix 2: exactly 100.00 also ships free
        return 0.0
    return SHIPPING_FEE


def invoice_total(lines: list[dict], discounts: dict[str, float]) -> float:
    """Discounted subtotal of every line with qty > 0, plus shipping, rounded to 2 dp."""
    subtotal = 0.0
    for line in lines:  # fix 3: range(1, ...) skipped the first line
        if line["qty"] <= 0:
            continue
        subtotal += line_total(line, discounts)
    return round(subtotal + shipping(subtotal), 2)
