def process(d):
    t = 0
    for i in d["items"]:
        if i["qty"] > 0:
            t = t + i["price_cents"] * i["qty"]
    x = 0
    if d.get("code"):
        if d["code"] == "SAVE10":
            x = t * 10 // 100
        else:
            if d["code"] == "FLAT5":
                if t >= 500:
                    x = 500
                else:
                    x = t
    for i in d["items"]:
        if i["qty"] > 0:
            a = i["price_cents"] * i["qty"]
            print(i["name"] + " x" + str(i["qty"]) + "  " + str(a // 100) + "." + str(a % 100).zfill(2))
    print("Subtotal  " + str(t // 100) + "." + str(t % 100).zfill(2))
    if x > 0:
        print("Discount  -" + str(x // 100) + "." + str(x % 100).zfill(2))
    print("Total  " + str((t - x) // 100) + "." + str((t - x) % 100).zfill(2))
    return t - x


# TODO: write these three pure helpers, then rewrite process() to use them.
def calculate_subtotal(items: list[dict]) -> int:
    return 0


def apply_discount(subtotal: int, code: str | None) -> int:
    return subtotal


def format_receipt(items: list[dict], subtotal: int, total: int) -> str:
    return ""


if __name__ == "__main__":
    order = {
        "items": [
            {"name": "Coffee", "price_cents": 350, "qty": 2},
            {"name": "Bagel", "price_cents": 250, "qty": 1},
            {"name": "Muffin", "price_cents": 300, "qty": 0},
        ],
        "code": "SAVE10",
    }
    print("returned", process(order))
