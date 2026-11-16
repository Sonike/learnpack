def split_name(filename: str) -> tuple[str, str]:
    """Split a file name into (stem, extension), e.g. "a.txt" -> ("a", ".txt")."""
    dot = filename.rfind(".")
    if dot <= 0:  # no dot at all, or a hidden file like ".bashrc"
        return (filename, "")
    return (filename[:dot], filename[dot:])


if __name__ == "__main__":
    for name in ["photo.jpg", "archive.tar.gz", ".bashrc", "Makefile", ".env.local"]:
        print(repr(name), "->", split_name(name))
