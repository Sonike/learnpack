from collections import deque
from string import ascii_lowercase


def word_ladder_length(begin: str, end: str, words: list[str]) -> int:
    """Number of words in the shortest one-letter-change path, or 0."""
    # TODO: BFS from (begin, 1); neighbours differ by one letter and are in words
    return 0


if __name__ == "__main__":
    print(word_ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))  # expected 5
