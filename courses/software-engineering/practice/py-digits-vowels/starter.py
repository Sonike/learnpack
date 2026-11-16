def sum_of_digits(n: int) -> int:
    """Return the sum of the digits of n, e.g. 1234 -> 10."""
    total = 0
    n = abs(n)
    # TODO: while n > 0: add the last digit (n % 10) to total, then drop it (n // 10)
    return total


def count_vowels(s: str) -> int:
    """Return how many characters in s are vowels (a, e, i, o, u), ignoring case."""
    count = 0
    # TODO: loop over each character; if its lowercase form is in "aeiou", add 1
    return count


if __name__ == "__main__":
    print(sum_of_digits(1234))          # 10
    print(count_vowels("Hello World"))  # 3
