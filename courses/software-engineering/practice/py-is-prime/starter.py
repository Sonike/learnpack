def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    # TODO: numbers below 2 are not prime
    # TODO: try divisors d = 2, 3, 4, ... while d * d <= n; any that divides n means not prime
    # TODO: if no divisor was found, n is prime
    return False


if __name__ == "__main__":
    print([n for n in range(30) if is_prime(n)])   # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
