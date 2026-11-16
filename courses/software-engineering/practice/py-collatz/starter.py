def collatz_steps(n: int) -> int:
    """Return how many Collatz steps it takes for n to reach 1."""
    steps = 0
    # TODO: while n is not 1:
    #         if n is even, n = n // 2; otherwise n = 3 * n + 1
    #         count the step
    return steps


if __name__ == "__main__":
    print(collatz_steps(6))    # 8
    print(collatz_steps(27))   # 111
