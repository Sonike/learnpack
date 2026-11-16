import math

CANDIDATES = {
    "O(1)": lambda n: 1,
    "O(log n)": lambda n: math.log2(n),
    "O(n)": lambda n: n,
    "O(n log n)": lambda n: n * math.log2(n),
    "O(n^2)": lambda n: n * n,
}


def classify_growth(sizes: list[int], step_counts: list[int]) -> str:
    """Return the name in CANDIDATES whose ratios step/f(size) are the flattest."""
    best_name, best_spread = "", math.inf
    for name, f in CANDIDATES.items():
        ratios = [steps / f(n) for n, steps in zip(sizes, step_counts)]
        spread = max(ratios) / min(ratios)
        if spread < best_spread:
            best_name, best_spread = name, spread
    return best_name
