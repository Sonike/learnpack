def squares_of_evens(nums: list[int]) -> list[int]:
    """[1, 2, 3, 4] -> [4, 16]"""
    return [n * n for n in nums if n % 2 == 0]


def word_lengths(words: list[str]) -> dict[str, int]:
    """["hi", "there"] -> {"hi": 2, "there": 5}"""
    return {word: len(word) for word in words}


def initials(names: list[str]) -> set[str]:
    """["ada", "Alan", "grace", ""] -> {"A", "G"}"""
    return {name[0].upper() for name in names if name}


def flatten(grid: list[list]) -> list:
    """[[1, 2], [3], []] -> [1, 2, 3]"""
    return [item for row in grid for item in row]
