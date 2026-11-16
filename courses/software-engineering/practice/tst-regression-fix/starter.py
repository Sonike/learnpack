def check_regression(fn) -> None:
    """Fail (AssertionError) if fn(total_cents, people) has the lost-cents bug."""
    # TODO: assert something that is false for the buggy version
    pass


def split_bill(total_cents: int, people: int) -> list[int]:
    """Split a bill into shares that add up to total_cents exactly."""
    share = total_cents // people  # TODO: fix the lost cents (and reject people < 1)
    return [share] * people


if __name__ == "__main__":
    def buggy(total_cents, people):
        share = total_cents // people
        return [share] * people

    # Part 1: this must say "caught" before you fix anything.
    try:
        check_regression(buggy)
        print("the buggy version passed: your regression test doesn't catch the bug yet")
    except AssertionError as e:
        print("caught:", e)

    # Part 2: once split_bill is fixed, this must pass.
    check_regression(split_bill)
    print(split_bill(1000, 3))
