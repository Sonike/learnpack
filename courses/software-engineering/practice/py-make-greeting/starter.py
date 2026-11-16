# TODO: add a bare * so that formal and title are keyword-only
def make_greeting(name: str, formal: bool = False, title: str | None = None) -> str:
    """Return an informal or formal greeting, with an optional title before the name."""
    # TODO: who = name, or f"{title} {name}" when title is not None
    # TODO: formal -> "Good day, <who>."   informal -> "Hi, <who>!"
    return ""


if __name__ == "__main__":
    print(make_greeting("Sam"))
    print(make_greeting("Okafor", formal=True, title="Dr"))
