def code_points(text: str) -> list[int]:
    """Return the Unicode code point of each character, e.g. "Hi" -> [72, 105]."""
    return [ord(ch) for ch in text]


def utf8_byte_count(text: str) -> int:
    """Return how many bytes text takes in UTF-8."""
    return len(text.encode("utf-8"))


if __name__ == "__main__":
    for word in ["Hi!", "café", "日本", "🙂"]:
        print(repr(word), "characters:", len(word), "code points:", code_points(word), "bytes:", utf8_byte_count(word))
