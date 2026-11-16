from collections import deque
from string import ascii_lowercase


def word_ladder_length(begin: str, end: str, words: list[str]) -> int:
    """Number of words in the shortest one-letter-change path, or 0."""
    unvisited = set(words)
    if end not in unvisited:
        return 0
    queue = deque([(begin, 1)])
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            for letter in ascii_lowercase:
                candidate = word[:i] + letter + word[i + 1:]
                if candidate in unvisited:
                    unvisited.remove(candidate)
                    queue.append((candidate, steps + 1))
    return 0
