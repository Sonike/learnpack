def run(commands: list[str]) -> list[str]:
    """Run shell-like commands on an in-memory folder tree and return the output lines."""
    root = {}      # each folder is a dict: child name -> child folder (another dict)
    path = []      # names of the folders from the root down to where we are, e.g. ["notes", "2026"]
    output = []

    for line in commands:
        words = line.split()
        if not words:
            continue

        current = root
        for name in path:
            current = current[name]

        command = words[0]
        if command == "pwd":
            output.append("/" + "/".join(path))
        elif command == "ls":
            output.extend(sorted(current))
        elif command == "mkdir":
            name = words[1]
            if name in current:
                output.append(f"mkdir: {name}: File exists")
            else:
                current[name] = {}
        elif command == "cd":
            target = words[1]
            if target == "/":
                path = []
            elif target == "..":
                if path:
                    path.pop()
            elif target in current:
                path.append(target)
            else:
                output.append(f"cd: no such file or directory: {target}")
        else:
            output.append(f"command not found: {command}")

    return output


if __name__ == "__main__":
    for line in run(["mkdir notes", "mkdir code", "ls", "cd notes", "pwd", "cd music", "cd ..", "pwd"]):
        print(line)
