def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Return {length: [words of that length, in input order]}."""
    groups = {}
    for word in words:
        # TODO: if len(word) isn't a key yet, start it with an empty list
        # TODO: append the word to that list
        pass
    return groups


if __name__ == "__main__":
    print(group_by_length(["hi", "cat", "a", "dog", "ok"]))
