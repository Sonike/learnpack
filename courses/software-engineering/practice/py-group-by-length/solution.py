def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Return {length: [words of that length, in input order]}."""
    groups = {}
    for word in words:
        length = len(word)
        if length not in groups:
            groups[length] = []
        groups[length].append(word)
    return groups


if __name__ == "__main__":
    print(group_by_length(["hi", "cat", "a", "dog", "ok"]))
