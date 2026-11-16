def sum_of_digits(n: int) -> int:
    """Return the sum of the digits of n, e.g. 1234 -> 10."""
    total = 0
    n = abs(n)
    while n > 0:
        total += n % 10
        n //= 10
    return total


def count_vowels(s: str) -> int:
    """Return how many characters in s are vowels (a, e, i, o, u), ignoring case."""
    count = 0
    for ch in s:
        if ch.lower() in "aeiou":
            count += 1
    return count


if __name__ == "__main__":
    print(sum_of_digits(1234))          # 10
    print(count_vowels("Hello World"))  # 3
