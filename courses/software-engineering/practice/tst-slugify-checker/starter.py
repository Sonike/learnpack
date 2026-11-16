def check_slugify(fn) -> None:
    """Assert that fn(title) follows the slug rules. Raise AssertionError if it doesn't."""
    cases = [
        ("Hello World", "hello-world"),
        # TODO: add a case for each rule and edge: accents, repeated separators,
        #       separators at both ends, punctuation, digits, underscores
    ]
    for title, want in cases:
        got = fn(title)
        assert got == want, f"slugify({title!r}): expected {want!r}, got {got!r}"


if __name__ == "__main__":
    import re

    def keeps_capitals(title):
        return re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")

    try:
        check_slugify(keeps_capitals)
        print("keeps_capitals slipped through: add a case that catches it")
    except AssertionError as e:
        print("caught:", e)
