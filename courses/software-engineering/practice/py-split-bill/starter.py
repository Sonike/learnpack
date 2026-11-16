def split_bill(total: float, people: int, tip_percent: float) -> float:
    """Return each person's share of total plus tip, rounded to cents."""
    # TODO: work out the tip, add it to the total, divide by people
    # TODO: round to 2 decimal places at the very end
    return 0.0


if __name__ == "__main__":
    print(split_bill(100, 4, 0))    # 25.0
    print(split_bill(100, 3, 0))    # 33.33
    print(split_bill(120, 4, 15))   # 34.5
