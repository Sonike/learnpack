def to_binary(n: int) -> str:
    """Return the binary digits of n (n >= 0) as a string, e.g. 5 -> "101"."""
    # TODO: handle n == 0 first
    # TODO: loop while n > 0: take n % 2, then n = n // 2
    # TODO: the bits come out last-first, so reverse them before joining
    return ""


def from_binary(s: str) -> int:
    """Return the number a string of 0s and 1s stands for, e.g. "101" -> 5."""
    # TODO: start with total = 0; for each digit, total = total * 2 + int(digit)
    return 0


if __name__ == "__main__":
    for n in [0, 1, 2, 5, 13, 255]:
        print(n, "->", repr(to_binary(n)), "  built-in says", bin(n)[2:])
    print(from_binary("1101"), "(should be 13)")
