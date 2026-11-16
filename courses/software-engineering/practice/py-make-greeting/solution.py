def make_greeting(name: str, *, formal: bool = False, title: str | None = None) -> str:
    """Return an informal or formal greeting, with an optional title before the name."""
    who = name if title is None else f"{title} {name}"
    if formal:
        return f"Good day, {who}."
    return f"Hi, {who}!"


if __name__ == "__main__":
    print(make_greeting("Sam"))
    print(make_greeting("Okafor", formal=True, title="Dr"))
