def add(numbers: str) -> int:
    """Sum the numbers in a string. See the prompt for the five stages."""
    if not numbers:
        return 0
    separators = ["\n"]
    if numbers.startswith("//"):
        header, numbers = numbers.split("\n", 1)
        separators.append(header[2:])
    for separator in separators:
        numbers = numbers.replace(separator, ",")
    values = [int(part) for part in numbers.split(",")]
    negatives = [n for n in values if n < 0]
    if negatives:
        raise ValueError("negatives not allowed: " + ", ".join(str(n) for n in negatives))
    return sum(values)


if __name__ == "__main__":
    assert add("//;\n1;2") == 3
    print(add("1\n2,3"))
