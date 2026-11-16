def title_case(s: str, minor_words: set[str]) -> str:
    """Capitalise each word, except minor words that aren't first."""
    result = []
    for i, word in enumerate(s.split()):
        word = word.lower()
        if i > 0 and word in minor_words:
            result.append(word)
        else:
            result.append(word.capitalize())
    return " ".join(result)


if __name__ == "__main__":
    print(title_case("the lord of the rings", {"of", "the"}))   # The Lord of the Rings
