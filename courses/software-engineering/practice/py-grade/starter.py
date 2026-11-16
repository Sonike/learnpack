def grade(score: int) -> str:
    """Return the letter grade (A-F) for a score from 0 to 100."""
    # TODO: if score is below 0 or above 100, raise ValueError
    # TODO: use if/elif/else, checking from the top grade down
    return "F"


if __name__ == "__main__":
    for s in [100, 90, 89, 75, 60, 59, 0]:
        print(s, grade(s))
