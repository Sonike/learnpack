def check_slugify(fn) -> None:
    """Assert that fn(title) follows the slug rules. Raise AssertionError if it doesn't."""
    cases = [
        ("Hello World", "hello-world"),            # ordinary case, capitals
        ("Café au lait", "cafe-au-lait"),          # accents become ASCII
        ("a -- b", "a-b"),                         # a run of separators is one dash
        ("  hello  ", "hello"),                    # no dashes at either end
        ("Rock & Roll!", "rock-roll"),             # punctuation is a separator
        ("Top 10 Tips", "top-10-tips"),            # digits are kept
        ("snake_case", "snake-case"),              # underscores are separators
        ("", ""),                                  # empty input
    ]
    for title, want in cases:
        got = fn(title)
        assert got == want, f"slugify({title!r}): expected {want!r}, got {got!r}"


if __name__ == "__main__":
    import re
    import unicodedata

    def slugify(title):
        plain = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
        return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")

    check_slugify(slugify)
    print("correct version passed")
