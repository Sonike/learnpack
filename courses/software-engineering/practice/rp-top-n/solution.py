from collections import Counter


def top_n(words: list[str], n: int) -> list[tuple[str, int]]:
    """The n most common words (case-insensitive) as (word, count), most common first."""
    if n <= 0:
        return []
    counts = Counter(word.lower() for word in words if word)
    return counts.most_common(n)
