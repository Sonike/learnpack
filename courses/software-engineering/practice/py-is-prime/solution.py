def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


if __name__ == "__main__":
    print([n for n in range(30) if is_prime(n)])   # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
