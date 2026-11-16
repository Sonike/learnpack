from solution import word_counts


def test_counts_repeated_words():
    got = word_counts("a b a c a b")
    want = {"a": 3, "b": 2, "c": 1}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_ignores_case():
    got = word_counts("The THE the")
    assert got == {"the": 3}, f"expected {{'the': 3}}, got {got!r}"


def test_strips_punctuation_from_word_ends():
    got = word_counts("The cat saw the other cat. THE END!")
    want = {"the": 3, "cat": 2, "saw": 1, "other": 1, "end": 1}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_keeps_apostrophes_inside_words_and_skips_lone_punctuation():
    got = word_counts("Don't stop - don't!")
    want = {"don't": 2, "stop": 1}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_empty_text_gives_empty_dict():
    for text in ["", "   ", "!!! ..."]:
        got = word_counts(text)
        assert got == {}, f"word_counts({text!r}): expected {{}}, got {got!r}"
