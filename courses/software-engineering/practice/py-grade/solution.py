def grade(score: int) -> str:
    """Return the letter grade (A-F) for a score from 0 to 100."""
    if score < 0 or score > 100:
        raise ValueError(f"score must be between 0 and 100, got {score}")
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


if __name__ == "__main__":
    for s in [100, 90, 89, 75, 60, 59, 0]:
        print(s, grade(s))
