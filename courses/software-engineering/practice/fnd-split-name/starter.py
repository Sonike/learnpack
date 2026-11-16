def split_name(filename: str) -> tuple[str, str]:
    """Split a file name into (stem, extension), e.g. "a.txt" -> ("a", ".txt")."""
    # TODO: find the position of the LAST dot with filename.rfind(".")
    # TODO: no dot (-1), or the only dot is the first character (0) -> no extension
    # TODO: otherwise slice: everything before the dot, and the dot plus everything after
    return (filename, "")


if __name__ == "__main__":
    for name in ["photo.jpg", "archive.tar.gz", ".bashrc", "Makefile", ".env.local"]:
        print(repr(name), "->", split_name(name))
