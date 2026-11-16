SUBJECT_LIMIT = 50
BODY_LIMIT = 72
IMPERATIVE_EXCEPTIONS = {"embed", "feed", "need", "seed", "speed", "bring", "ping", "string"}


def check_commit_message(msg: str) -> list[str]:
    """Return the problems with a commit message (an empty list means it's good)."""
    lines = [line for line in msg.splitlines() if not line.startswith("#")]
    # TODO: drop trailing blank lines; if nothing is left return ["Message is empty"]
    problems = []
    # TODO: subject = lines[0]; check length, capital, period and imperative mood
    # TODO: if there's a line 2, it must be blank
    # TODO: every line after the subject: at most BODY_LIMIT characters
    return problems


if __name__ == "__main__":
    print(check_commit_message("Add password reset email\n\nUsers had to email support to get back in."))
    print(check_commit_message("fixed the login bug that happened when the password was empty."))
