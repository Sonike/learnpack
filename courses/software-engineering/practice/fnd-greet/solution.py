def greet(name: str) -> str:
    """Return a friendly greeting for name, e.g. "ada" -> "Hello, Ada!"."""
    clean = name.strip().title()
    if not clean:
        clean = "stranger"
    return f"Hello, {clean}!"


if __name__ == "__main__":
    print(greet("ada"))
    print(greet("  grace HOPPER "))
    print(greet("   "))
