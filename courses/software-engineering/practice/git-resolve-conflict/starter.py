def resolve_conflict(text: str, choose: str) -> str:
    """Replace every conflict block with "ours", "theirs" or "both"; raise ValueError on bad markers."""
    if choose not in ("ours", "theirs", "both"):
        raise ValueError(f"choose must be 'ours', 'theirs' or 'both', got {choose!r}")
    out = []
    state = "outside"
    ours, theirs = [], []
    for line in text.splitlines(keepends=True):
        marker = line.rstrip("\r\n")
        # TODO: "<<<<<<<" -> start a block (error if already inside one)
        # TODO: "=======" -> switch from ours to theirs (error anywhere else)
        # TODO: ">>>>>>>" -> end the block: add the chosen lines to out (error unless in theirs)
        # TODO: any other line goes to out, ours or theirs depending on state
        out.append(line)
    # TODO: error if the file ended inside a block
    return "".join(out)


if __name__ == "__main__":
    text = (
        "def greet(name):\n"
        "<<<<<<< HEAD\n"
        '    greeting = "Hello"\n'
        "=======\n"
        '    greeting = "Hi there"\n'
        ">>>>>>> feature\n"
        '    return f"{greeting}, {name}!"\n'
    )
    for choice in ("ours", "theirs", "both"):
        print(f"--- {choice} ---")
        print(resolve_conflict(text, choice))
