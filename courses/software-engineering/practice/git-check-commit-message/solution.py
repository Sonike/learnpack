SUBJECT_LIMIT = 50
BODY_LIMIT = 72
IMPERATIVE_EXCEPTIONS = {"embed", "feed", "need", "seed", "speed", "bring", "ping", "string"}


def looks_imperative(subject: str) -> bool:
    """Heuristic: "Added"/"Fixing" are not imperative; "Add"/"Fix" are."""
    first_word = subject.split()[0].lower() if subject.split() else ""
    if first_word in IMPERATIVE_EXCEPTIONS:
        return True
    return not first_word.endswith(("ed", "ing"))


def check_commit_message(msg: str) -> list[str]:
    """Return the problems with a commit message (an empty list means it's good)."""
    lines = [line for line in msg.splitlines() if not line.startswith("#")]
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return ["Message is empty"]

    problems = []
    subject = lines[0]
    if len(subject) > SUBJECT_LIMIT:
        problems.append(f"Subject is {len(subject)} characters (keep it to {SUBJECT_LIMIT})")
    if subject[:1].islower():
        problems.append("Capitalize the subject line")
    if subject.endswith("."):
        problems.append("Do not end the subject with a period")
    if not looks_imperative(subject):
        problems.append('Use the imperative mood ("Fix bug", not "Fixed bug")')

    if len(lines) > 1 and lines[1].strip():
        problems.append("Separate subject from body with a blank line")
    for number, line in enumerate(lines[1:], start=2):
        if len(line) > BODY_LIMIT:
            problems.append(f"Body line {number} is {len(line)} characters (wrap at {BODY_LIMIT})")
    return problems
