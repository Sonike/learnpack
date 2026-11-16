from solution import check_is_leap_year


def correct(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


MUTANTS = {
    "only checks divisible by 4": lambda y: y % 4 == 0,
    "forgets the 400 exception": lambda y: y % 4 == 0 and y % 100 != 0,
    "only checks divisible by 400": lambda y: y % 400 == 0,
    "says every year is a leap year": lambda y: True,
    "swaps the 100 and 400 rules": lambda y: (y % 4 == 0 and y % 400 != 0) or y % 100 == 0,
}


def caught(mutant):
    try:
        check_is_leap_year(mutant)
    except Exception:
        return True
    return False


def test_correct_version_passes():
    try:
        check_is_leap_year(correct)
    except AssertionError as e:
        raise AssertionError(f"your checker rejected a correct leap-year function: {e}") from None


def test_catches_a_function_that_only_checks_by_4():
    assert caught(MUTANTS["only checks divisible by 4"]), "missed a bug: `year % 4 == 0` passed your checker. Try a century like 1900."


def test_catches_a_function_that_forgets_the_400_rule():
    assert caught(MUTANTS["forgets the 400 exception"]), "missed a bug: a function that says 2000 is not a leap year passed your checker"


def test_catches_a_function_that_only_checks_by_400():
    assert caught(MUTANTS["only checks divisible by 400"]), "missed a bug: `year % 400 == 0` passed your checker. Try an ordinary leap year."


def test_catches_a_function_that_always_says_yes():
    assert caught(MUTANTS["says every year is a leap year"]), "missed a bug: a function returning True for every year passed your checker"


def test_catches_swapped_century_rules():
    assert caught(MUTANTS["swaps the 100 and 400 rules"]), "missed a bug: a function with the 100 and 400 rules swapped passed your checker"
