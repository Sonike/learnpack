FREE_SHIPPING_FROM = 100.00
SHIPPING_FEE = 5.00


def line_total(line: dict, discounts: dict[str, float]) -> float:
    """price * qty, minus the line's discount (a percentage) if its sku has one."""
    subtotal = line["price"] * line["qty"]
    percent = discounts.get(line["sku"], 0)
    return subtotal * percent / 100


def shipping(subtotal: float) -> float:
    """Free from 100.00 upwards, otherwise 5.00. An empty order has no shipping."""
    if subtotal == 0:
        return 0.0
    if subtotal > FREE_SHIPPING_FROM:
        return 0.0
    return SHIPPING_FEE


def invoice_total(lines: list[dict], discounts: dict[str, float]) -> float:
    """Discounted subtotal of every line with qty > 0, plus shipping, rounded to 2 dp."""
    subtotal = 0.0
    for i in range(1, len(lines)):
        line = lines[i]
        if line["qty"] <= 0:
            continue
        subtotal += line_total(line, discounts)
    return round(subtotal + shipping(subtotal), 2)


if __name__ == "__main__":
    order = [
        {"sku": "pen", "price": 2.50, "qty": 4},
        {"sku": "book", "price": 40.00, "qty": 2},
    ]
    print(invoice_total(order, {"book": 25}))
    # want 75.0: pens 10.00 + books 60.00 = 70.00, plus 5.00 shipping
