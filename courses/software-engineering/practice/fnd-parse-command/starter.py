import shlex


def parse_command(line: str) -> tuple[str, list[str], list[str]]:
    """Split a command line into (command, flags, arguments)."""
    words = shlex.split(line)
    # TODO: an empty list of words -> return ("", [], [])
    # TODO: the first word is the command
    # TODO: sort the rest into flags (start with "-") and arguments (everything else)
    return ("", [], [])


if __name__ == "__main__":
    print(parse_command("ls -la projects"))
    print(parse_command('cp -r "My Documents" backup --verbose'))
