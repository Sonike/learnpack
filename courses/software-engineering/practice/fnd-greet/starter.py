def greet(name: str) -> str:
    """Return a friendly greeting for name, e.g. "ada" -> "Hello, Ada!"."""
    # TODO: clean the name with .strip() and .title()
    # TODO: if the cleaned name is empty, use "stranger" instead
    # TODO: return the greeting (don't print it)
    return "Hello!"


if __name__ == "__main__":
    print(greet("ada"))
    print(greet("  grace HOPPER "))
    print(greet("   "))
