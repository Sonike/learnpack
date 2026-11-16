import string


def word_counts(text: str) -> dict[str, int]:
    """Return how many times each word appears, ignoring case and surrounding punctuation."""
    counts = {}
    for word in text.split():
        word = word.lower().strip(string.punctuation)
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts


if __name__ == "__main__":
    print(word_counts("The cat saw the other cat. THE END!"))
