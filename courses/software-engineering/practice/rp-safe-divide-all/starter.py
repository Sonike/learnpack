def safe_divide_all(pairs: list[tuple]) -> tuple[list[float], list[str]]:
    """Divide every (a, b) pair. Return (results, errors) instead of crashing."""
    results = []
    errors = []
    # TODO: loop with enumerate(pairs) so you know each pair's index
    # TODO: try a / b; on ZeroDivisionError or TypeError add f"pair {i}: {e}" to errors
    # TODO: use else: to append the answer to results only when it worked
    return results, errors


if __name__ == "__main__":
    results, errors = safe_divide_all([(10, 2), (1, 0), ("6", 2), (9, 3)])
    print("results:", results)
    print("errors:", errors)
