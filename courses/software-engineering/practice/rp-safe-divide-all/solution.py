def safe_divide_all(pairs: list[tuple]) -> tuple[list[float], list[str]]:
    """Divide every (a, b) pair. Return (results, errors) instead of crashing."""
    results = []
    errors = []
    for i, (a, b) in enumerate(pairs):
        try:
            answer = a / b
        except (ZeroDivisionError, TypeError) as e:
            errors.append(f"pair {i}: {e}")
        else:
            results.append(answer)
    return results, errors
