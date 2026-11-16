from solution import slugify

CASES = [
    ("Hello World", "hello-world"),
    ("Café au Lait: 10 Tips!", "cafe-au-lait-10-tips"),
    ("  Leading and trailing  ", "leading-and-trailing"),
    ("a -- b __ c", "a-b-c"),
    ("snake_case_name", "snake-case-name"),
    ("Ünïcödé Rocks", "unicode-rocks"),
]


def test_table_of_ordinary_titles():
    for title, want in CASES:
        got = slugify(title)
        assert got == want, f"slugify({title!r}): expected {want!r}, got {got!r}"


def test_title_without_letters_gives_empty_slug():
    got = slugify("!!!")
    assert got == "", f"expected '', got {got!r}"


def test_empty_title_gives_empty_slug():
    got = slugify("")
    assert got == "", f"expected '', got {got!r}"


def test_digits_are_kept():
    got = slugify("Top 10 of 2025")
    assert got == "top-10-of-2025", f"expected 'top-10-of-2025', got {got!r}"
