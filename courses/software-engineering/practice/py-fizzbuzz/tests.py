from solution import fizzbuzz


def test_first_five():
    got = fizzbuzz(5)
    want = ["1", "2", "Fizz", "4", "Buzz"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_fifteen_is_fizzbuzz():
    got = fizzbuzz(15)
    want = ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
            "11", "Fizz", "13", "14", "FizzBuzz"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_length_matches_n():
    got = len(fizzbuzz(100))
    assert got == 100, f"expected 100 items, got {got!r}"


def test_zero_gives_empty_list():
    got = fizzbuzz(0)
    assert got == [], f"expected [], got {got!r}"


def test_numbers_are_strings():
    got = fizzbuzz(1)
    assert got == ["1"], f"expected ['1'] (a string, not the int 1), got {got!r}"
