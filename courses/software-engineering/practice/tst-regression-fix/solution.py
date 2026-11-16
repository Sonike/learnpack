def check_regression(fn) -> None:
    """Fail (AssertionError) if fn(total_cents, people) has the lost-cents bug."""
    for total, people in [(1000, 3), (1001, 3), (100, 7), (999, 1)]:
        shares = fn(total, people)
        assert sum(shares) == total, f"split_bill({total}, {people}) = {shares}, which adds up to {sum(shares)}, not {total}"
        assert len(shares) == people, f"split_bill({total}, {people}) should give {people} shares, got {len(shares)}"


def split_bill(total_cents: int, people: int) -> list[int]:
    """Split a bill into shares that add up to total_cents exactly."""
    if people < 1:
        raise ValueError("need at least one person")
    share, leftover = divmod(total_cents, people)
    return [share + 1 if i < leftover else share for i in range(people)]


if __name__ == "__main__":
    check_regression(split_bill)
    print(split_bill(1000, 3))
