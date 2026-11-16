def resolve_conflict(text: str, choose: str) -> str:
    """Replace every conflict block with "ours", "theirs" or "both"; raise ValueError on bad markers."""
    if choose not in ("ours", "theirs", "both"):
        raise ValueError(f"choose must be 'ours', 'theirs' or 'both', got {choose!r}")
    out = []
    state = "outside"
    ours, theirs = [], []
    for number, line in enumerate(text.splitlines(keepends=True), start=1):
        marker = line.rstrip("\r\n")
        if marker.startswith("<<<<<<<"):
            if state != "outside":
                raise ValueError(f"line {number}: '<<<<<<<' inside a conflict block")
            state, ours, theirs = "ours", [], []
        elif marker == "=======":
            if state != "ours":
                raise ValueError(f"line {number}: '=======' without a matching '<<<<<<<'")
            state = "theirs"
        elif marker.startswith(">>>>>>>"):
            if state != "theirs":
                raise ValueError(f"line {number}: '>>>>>>>' without '<<<<<<<' and '======='")
            if choose in ("ours", "both"):
                out.extend(ours)
            if choose in ("theirs", "both"):
                out.extend(theirs)
            state = "outside"
        elif state == "ours":
            ours.append(line)
        elif state == "theirs":
            theirs.append(line)
        else:
            out.append(line)
    if state != "outside":
        raise ValueError("the file ends inside a conflict block")
    return "".join(out)
