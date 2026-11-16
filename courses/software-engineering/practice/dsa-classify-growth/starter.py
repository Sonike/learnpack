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
    # TODO: for each name, f in CANDIDATES.items():
    #         ratios = [steps / f(n) for n, steps in zip(sizes, step_counts)]
    #         spread = max(ratios) / min(ratios)
    # TODO: return the name with the smallest spread
    return "O(1)"


if __name__ == "__main__":
    sizes = [1000, 2000, 4000, 8000]
    print(classify_growth(sizes, [3 * n + 5 for n in sizes]))             # want O(n)
    print(classify_growth(sizes, [n * n for n in sizes]))                 # want O(n^2)
    print(classify_growth(sizes, [int(n * math.log2(n)) for n in sizes]))  # want O(n log n)
