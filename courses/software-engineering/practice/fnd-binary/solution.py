def to_binary(n: int) -> str:
    """Return the binary digits of n (n >= 0) as a string, e.g. 5 -> "101"."""
    if n == 0:
        return "0"
    bits = []
    while n > 0:
        bits.append(str(n % 2))  # the last bit
        n = n // 2               # drop the last bit
    bits.reverse()
    return "".join(bits)


def from_binary(s: str) -> int:
    """Return the number a string of 0s and 1s stands for, e.g. "101" -> 5."""
    total = 0
    for digit in s:
        total = total * 2 + int(digit)
    return total


if __name__ == "__main__":
    for n in [0, 1, 2, 5, 13, 255]:
        print(n, "->", repr(to_binary(n)), "  built-in says", bin(n)[2:])
    print(from_binary("1101"), "(should be 13)")
