def resolve(cwd: str, path: str) -> str:
    """Return the absolute, clean version of path, as seen from the folder cwd."""
    if path.startswith("/"):
        parts = []
    else:
        parts = [p for p in cwd.split("/") if p]

    for piece in path.split("/"):
        if piece in ("", "."):
            continue
        if piece == "..":
            if parts:
                parts.pop()
        else:
            parts.append(piece)

    return "/" + "/".join(parts)


if __name__ == "__main__":
    print(resolve("/home/ada", "projects/app"))      # /home/ada/projects/app
    print(resolve("/home/ada/projects", "../data"))  # /home/ada/data
    print(resolve("/home/ada", "/etc//hosts/"))      # /etc/hosts
    print(resolve("/", "../.."))                     # /
