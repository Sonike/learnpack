def fizzbuzz(n: int) -> list[str]:
    """Return the FizzBuzz strings for 1..n."""
    result = []
    for number in range(1, n + 1):
        if number % 3 == 0 and number % 5 == 0:
            result.append("FizzBuzz")
        elif number % 3 == 0:
            result.append("Fizz")
        elif number % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(number))
    return result


if __name__ == "__main__":
    print(fizzbuzz(15))
