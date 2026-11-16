def run(commands: list[str]) -> list[str]:
    """Run shell-like commands on an in-memory folder tree and return the output lines."""
    root = {}      # each folder is a dict: child name -> child folder (another dict)
    path = []      # names of the folders from the root down to where we are, e.g. ["notes", "2026"]
    output = []

    for line in commands:
        words = line.split()
        if not words:
            continue
        # TODO: find the current folder by walking from root through each name in path
        # TODO: handle "pwd", "ls", "mkdir NAME", "cd NAME", "cd ..", "cd /"
        # TODO: anything else -> output.append(f"command not found: {words[0]}")

    return output


if __name__ == "__main__":
    for line in run(["mkdir notes", "mkdir code", "ls", "cd notes", "pwd", "cd music", "cd ..", "pwd"]):
        print(line)
