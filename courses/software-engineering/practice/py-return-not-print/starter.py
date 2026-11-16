def average(numbers: list[float]) -> float | None:
    """Return the mean of numbers, or None for an empty list."""
    # TODO: this prints instead of returning, and crashes on []
    print(sum(numbers) / len(numbers))


def format_price(amount: float) -> str:
    """Return amount as dollars with two decimal places, e.g. 3.5 -> "$3.50"."""
    # TODO: this prints instead of returning
    print(f"${amount:.2f}")


if __name__ == "__main__":
    result = average([1, 2, 3, 4])
    print("average returned:", result)        # should say 2.5, not None
    print("format_price returned:", format_price(3.5))
