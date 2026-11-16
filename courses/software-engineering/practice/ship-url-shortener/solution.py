ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)


def encode(n: int) -> str:
    """Write a whole number in base62."""
    if n < 0:
        raise ValueError("n must be 0 or more")
    if n == 0:
        return ALPHABET[0]
    digits = []
    while n > 0:
        n, remainder = divmod(n, BASE)
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


def decode(code: str) -> int:
    """Turn a base62 code back into its number."""
    if not code or any(char not in ALPHABET for char in code):
        raise ValueError(f"invalid code: {code!r}")
    value = 0
    for char in code:
        value = value * BASE + ALPHABET.index(char)
    return value


class URLShortener:
    def __init__(self):
        self.next_id = 1
        self.urls = {}    # id -> url
        self.codes = {}   # url -> code

    def shorten(self, url: str) -> str:
        """Return the short code for url (the same code if seen before)."""
        if url in self.codes:
            return self.codes[url]
        code = encode(self.next_id)
        self.urls[self.next_id] = url
        self.codes[url] = code
        self.next_id += 1
        return code

    def expand(self, code: str) -> str | None:
        """Return the original URL, or None if the code is unknown."""
        try:
            return self.urls.get(decode(code))
        except ValueError:
            return None
