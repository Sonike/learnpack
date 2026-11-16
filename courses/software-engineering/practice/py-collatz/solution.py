def collatz_steps(n: int) -> int:
    """Return how many Collatz steps it takes for n to reach 1."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


if __name__ == "__main__":
    print(collatz_steps(6))    # 8
    print(collatz_steps(27))   # 111
