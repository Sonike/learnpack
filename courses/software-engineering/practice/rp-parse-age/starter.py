def parse_age(s: str) -> int:
    """Turn user-typed text into an age from 0 to 150, or raise ValueError."""
    # TODO: strip whitespace and try int(...); on ValueError raise your own
    #       ValueError(f"age must be a whole number, got {s!r}") from None
    # TODO: check the range and raise ValueError mentioning "between 0 and 150"
    return 0


if __name__ == "__main__":
    for text in [" 42 ", "abc", "200", "-1", ""]:
        try:
            print(repr(text), "->", parse_age(text))
        except ValueError as e:
            print(repr(text), "-> ValueError:", e)
