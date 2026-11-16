from dataclasses import dataclass

GRAMS_PER_KG = 1000


@dataclass(frozen=True)
class Rate:
    base_cents: int
    per_kg_cents: int


RATES: dict[str, Rate] = {
    "local": Rate(300, 50),
    "regional": Rate(450, 75),
    "national": Rate(600, 100),
    "europe": Rate(1300, 250),
    "north-america": Rate(1800, 350),
    "asia": Rate(2000, 400),
    "rest-of-world": Rate(2500, 500),
}


def shipping_cost(zone: str, weight_g: int) -> int:
    if weight_g <= 0:
        raise ValueError("weight must be positive")
    if zone not in RATES:
        raise ValueError(f"unknown zone: {zone}")
    rate = RATES[zone]
    kg = -(-weight_g // GRAMS_PER_KG)  # round up to whole kilograms
    return rate.base_cents + rate.per_kg_cents * kg


if __name__ == "__main__":
    print(shipping_cost("local", 500), shipping_cost("europe", 2500))
