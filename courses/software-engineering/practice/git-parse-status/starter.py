def parse_status_porcelain(text: str) -> dict[str, list[str]]:
    """Group `git status --porcelain` lines into staged, modified and untracked paths."""
    result = {"staged": [], "modified": [], "untracked": []}
    for line in text.splitlines():
        # TODO: skip blank lines
        # TODO: x, y = line[0], line[1]; path = line[3:] (for "old -> new" keep the new name)
        # TODO: "??" -> untracked, "!!" -> skip
        # TODO: x is a letter -> staged; y is a letter -> modified (both can be true)
        pass
    return result


if __name__ == "__main__":
    sample = "M  app.py\n M README.md\nMM utils.py\nA  tests/test_app.py\nR  old_name.py -> new_name.py\n?? notes.txt\n"
    print(parse_status_porcelain(sample))
