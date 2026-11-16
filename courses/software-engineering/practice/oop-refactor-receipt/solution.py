SAVE10_PERCENT = 10
FLAT5_CENTS = 500


def _money(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}"


def _counted(items: list[dict]) -> list[dict]:
    """Items that are actually being bought (qty above zero)."""
    return [item for item in items if item["qty"] > 0]


def calculate_subtotal(items: list[dict]) -> int:
    return sum(item["price_cents"] * item["qty"] for item in _counted(items))


def apply_discount(subtotal: int, code: str | None) -> int:
    if code == "SAVE10":
        return subtotal - subtotal * SAVE10_PERCENT // 100
    if code == "FLAT5":
        return subtotal - min(FLAT5_CENTS, subtotal)
    return subtotal


def format_receipt(items: list[dict], subtotal: int, total: int) -> str:
    lines = [f"{item['name']} x{item['qty']}  {_money(item['price_cents'] * item['qty'])}" for item in _counted(items)]
    lines.append(f"Subtotal  {_money(subtotal)}")
    discount = subtotal - total
    if discount > 0:
        lines.append(f"Discount  -{_money(discount)}")
    lines.append(f"Total  {_money(total)}")
    return "\n".join(lines)


def process(order: dict) -> int:
    subtotal = calculate_subtotal(order["items"])
    total = apply_discount(subtotal, order.get("code"))
    print(format_receipt(order["items"], subtotal, total))
    return total


if __name__ == "__main__":
    print(process({"items": [{"name": "Coffee", "price_cents": 350, "qty": 2}], "code": "SAVE10"}))
