ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)


def encode(n: int) -> str:
    """Write a whole number in base62."""
    # TODO: handle negative and 0; then divmod by 62 repeatedly
    return ""


def decode(code: str) -> int:
    """Turn a base62 code back into its number."""
    # TODO: value = value * 62 + ALPHABET.index(char); reject bad characters
    return 0


class URLShortener:
    def __init__(self):
        self.next_id = 1
        self.urls = {}    # id -> url
        self.codes = {}   # url -> code

    def shorten(self, url: str) -> str:
        """Return the short code for url (the same code if seen before)."""
        # TODO
        return ""

    def expand(self, code: str) -> str | None:
        """Return the original URL, or None if the code is unknown."""
        # TODO
        return None


if __name__ == "__main__":
    print(encode(61), encode(62), decode("21"))   # Z 10 125
    s = URLShortener()
    print(s.shorten("https://example.com/a"))     # 1
    print(s.shorten("https://example.com/b"))     # 2
    print(s.expand("2"))                          # https://example.com/b
