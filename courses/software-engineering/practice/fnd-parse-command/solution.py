import shlex


def parse_command(line: str) -> tuple[str, list[str], list[str]]:
    """Split a command line into (command, flags, arguments)."""
    words = shlex.split(line)
    if not words:
        return ("", [], [])

    command = words[0]
    flags = []
    arguments = []
    for word in words[1:]:
        if word.startswith("-"):
            flags.append(word)
        else:
            arguments.append(word)
    return (command, flags, arguments)


if __name__ == "__main__":
    print(parse_command("ls -la projects"))
    print(parse_command('cp -r "My Documents" backup --verbose'))
