from fnmatch import fnmatchcase


def matches(path: str, pattern: str) -> bool:
    """Does one pattern (without "!") match path? Rules 4-6 from the prompt."""
    parts = path.split("/")
    # TODO: pattern ends with "/": does any folder in parts[:-1] match pattern[:-1]?
    # TODO: pattern contains "/": match the whole path against pattern.lstrip("/")
    # TODO: otherwise: does any part of the path match?
    return False


def is_ignored(path: str, patterns: list[str]) -> bool:
    """Apply .gitignore patterns in order; the last match wins; "!" un-ignores."""
    ignored = False
    for pattern in patterns:
        # TODO: skip blank lines and comments
        # TODO: handle "!" and call matches(); update ignored when a pattern matches
        pass
    return ignored


if __name__ == "__main__":
    patterns = ["# Python", "__pycache__/", "*.pyc", ".env", "*.log", "!keep.log"]
    for path in ["app/__pycache__/app.cpython-312.pyc", ".env", "server.log", "keep.log", "app/main.py"]:
        print(path, "->", is_ignored(path, patterns))
