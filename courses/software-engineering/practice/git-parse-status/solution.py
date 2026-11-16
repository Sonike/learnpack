def parse_status_porcelain(text: str) -> dict[str, list[str]]:
    """Group `git status --porcelain` lines into staged, modified and untracked paths."""
    result = {"staged": [], "modified": [], "untracked": []}
    for line in text.splitlines():
        if not line.strip():
            continue
        x, y = line[0], line[1]
        path = line[3:]
        if " -> " in path:  # a rename: "old -> new"
            path = path.split(" -> ")[1]

        if x == "?" and y == "?":
            result["untracked"].append(path)
            continue
        if x == "!":  # ignored files only show up with --ignored
            continue
        if x != " ":
            result["staged"].append(path)
        if y != " ":
            result["modified"].append(path)
    return result
