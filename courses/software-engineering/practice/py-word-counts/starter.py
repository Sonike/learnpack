import string


def word_counts(text: str) -> dict[str, int]:
    """Return how many times each word appears, ignoring case and surrounding punctuation."""
    counts = {}
    for word in text.split():
        # TODO: clean the word: lowercase, then .strip(string.punctuation)
        # TODO: skip it if it's now empty
        # TODO: add 1 to its count (counts.get(word, 0) is handy)
        pass
    return counts


if __name__ == "__main__":
    print(word_counts("The cat saw the other cat. THE END!"))
