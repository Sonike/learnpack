from solution import code_points, utf8_byte_count


def test_code_points_of_plain_letters():
    got = code_points("Hi!")
    assert got == [72, 105, 33], f"expected [72, 105, 33], got {got!r}"


def test_code_points_of_accented_letter_and_emoji():
    got = code_points("é🙂")
    assert got == [233, 128578], f"expected [233, 128578], got {got!r}"


def test_ascii_text_is_one_byte_per_character():
    got = utf8_byte_count("hello world")
    assert got == 11, f"expected 11, got {got!r}"


def test_accented_letter_takes_two_bytes():
    got = utf8_byte_count("café")
    assert got == 5, f"expected 5, got {got!r}"


def test_chinese_characters_and_emoji():
    for text, want in [("日本", 6), ("🙂", 4), ("a🙂b", 6)]:
        got = utf8_byte_count(text)
        assert got == want, f"utf8_byte_count({text!r}): expected {want!r}, got {got!r}"


def test_empty_text_has_no_bytes_or_code_points():
    assert utf8_byte_count("") == 0, f"expected 0, got {utf8_byte_count('')!r}"
    assert code_points("") == [], f"expected [], got {code_points('')!r}"
