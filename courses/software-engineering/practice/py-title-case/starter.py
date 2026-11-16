def title_case(s: str, minor_words: set[str]) -> str:
    """Capitalise each word, except minor words that aren't first."""
    result = []
    # TODO: loop over the words of s.split() with enumerate() so you know which one is first
    # TODO: lowercase each word; keep it lowercase if it's minor and not first, else capitalize()
    # TODO: join with " "
    return s


if __name__ == "__main__":
    print(title_case("the lord of the rings", {"of", "the"}))   # The Lord of the Rings
