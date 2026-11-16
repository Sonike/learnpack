import dataclasses

import solution
from solution import shipping_cost


def test_prices_are_unchanged_for_every_zone():
    cases = [
        ("local", 500, 350), ("regional", 1000, 525), ("national", 1500, 800), ("europe", 2500, 2050),
        ("north-america", 1, 2150), ("asia", 3000, 3200), ("rest-of-world", 1001, 3500),
    ]
    for zone, weight, want in cases:
        got = shipping_cost(zone, weight)
        assert got == want, f"shipping_cost({zone!r}, {weight}): expected {want!r}, got {got!r}"


def test_rejects_unknown_zone():
    try:
        shipping_cost("mars", 100)
    except ValueError:
        return
    raise AssertionError("an unknown zone should raise ValueError")


def test_rejects_zero_or_negative_weight():
    for weight in (0, -5):
        try:
            shipping_cost("local", weight)
        except ValueError:
            continue
        raise AssertionError(f"weight {weight} should raise ValueError")


def test_rates_are_a_dict_of_rate_dataclasses():
    rates = getattr(solution, "RATES", None)
    assert isinstance(rates, dict) and len(rates) == 7, f"expected a RATES dict with 7 zones, got {rates!r}"
    assert dataclasses.is_dataclass(solution.Rate), "Rate should be a dataclass"
    assert all(isinstance(r, solution.Rate) for r in rates.values()), "every value in RATES should be a Rate"


def test_new_zone_needs_only_a_new_rate():
    solution.RATES["moon"] = solution.Rate(100_000, 1)
    try:
        got = shipping_cost("moon", 2000)
    finally:
        del solution.RATES["moon"]
    assert got == 100_002, f"after adding a 'moon' Rate, expected 100002, got {got!r} (does shipping_cost read RATES?)"
