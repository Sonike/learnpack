from dataclasses import dataclass


def shipping_cost(zone, weight_g):
    if weight_g <= 0:
        raise ValueError("weight must be positive")
    kg = -(-weight_g // 1000)
    if zone == "local":
        return 300 + 50 * kg
    elif zone == "regional":
        return 450 + 75 * kg
    elif zone == "national":
        return 600 + 100 * kg
    elif zone == "europe":
        return 1300 + 250 * kg
    elif zone == "north-america":
        return 1800 + 350 * kg
    elif zone == "asia":
        return 2000 + 400 * kg
    elif zone == "rest-of-world":
        return 2500 + 500 * kg
    else:
        raise ValueError(f"unknown zone: {zone}")


# TODO: a frozen Rate dataclass, a RATES dict with all seven zones,
#       and a shipping_cost that looks the zone up in RATES.


if __name__ == "__main__":
    print(shipping_cost("local", 500))    # 350
    print(shipping_cost("europe", 2500))  # 2050
