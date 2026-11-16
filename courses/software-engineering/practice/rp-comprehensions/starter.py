def squares_of_evens(nums: list[int]) -> list[int]:
    """[1, 2, 3, 4] -> [4, 16]"""
    # TODO: one list comprehension with an if
    return []


def word_lengths(words: list[str]) -> dict[str, int]:
    """["hi", "there"] -> {"hi": 2, "there": 5}"""
    # TODO: one dict comprehension
    return {}


def initials(names: list[str]) -> set[str]:
    """["ada", "Alan", "grace", ""] -> {"A", "G"}"""
    # TODO: one set comprehension; skip empty names
    return set()


def flatten(grid: list[list]) -> list:
    """[[1, 2], [3], []] -> [1, 2, 3]"""
    # TODO: one list comprehension with two for clauses
    return []


if __name__ == "__main__":
    print(squares_of_evens([1, 2, 3, 4]))
    print(word_lengths(["hi", "there"]))
    print(initials(["ada", "Alan", "grace", ""]))
    print(flatten([[1, 2], [3], []]))
