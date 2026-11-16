from fnmatch import fnmatchcase


def matches(path: str, pattern: str) -> bool:
    """Does one pattern (without "!") match path? Rules 4-6 from the prompt."""
    parts = path.split("/")
    if pattern.endswith("/"):
        folders = parts[:-1]
        return any(fnmatchcase(folder, pattern[:-1]) for folder in folders)
    if "/" in pattern:
        return fnmatchcase(path, pattern.lstrip("/"))
    return any(fnmatchcase(part, pattern) for part in parts)


def is_ignored(path: str, patterns: list[str]) -> bool:
    """Apply .gitignore patterns in order; the last match wins; "!" un-ignores."""
    ignored = False
    for pattern in patterns:
        pattern = pattern.strip()
        if not pattern or pattern.startswith("#"):
            continue
        negate = pattern.startswith("!")
        if negate:
            pattern = pattern[1:]
        if matches(path, pattern):
            ignored = not negate
    return ignored
