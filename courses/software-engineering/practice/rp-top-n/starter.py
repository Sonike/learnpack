from collections import Counter


def top_n(words: list[str], n: int) -> list[tuple[str, int]]:
    """The n most common words (case-insensitive) as (word, count), most common first."""
    # TODO: build a Counter from the lowercased, non-empty words
    # TODO: return counter.most_common(n), or [] when n <= 0
    return []


if __name__ == "__main__":
    text = "The cat sat on the mat and the dog sat on the cat"
    print(top_n(text.split(), 3))  # want [('the', 4), ('cat', 2), ('sat', 2)]
