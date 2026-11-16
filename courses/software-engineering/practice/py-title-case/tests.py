from solution import title_case

MINOR = {"a", "an", "and", "of", "the", "in", "on"}


def test_minor_words_stay_lowercase():
    got = title_case("the lord of the rings", {"of", "the"})
    assert got == "The Lord of the Rings", f"expected 'The Lord of the Rings', got {got!r}"


def test_first_word_is_always_capitalised():
    got = title_case("a tale of two cities", MINOR)
    assert got == "A Tale of Two Cities", f"expected 'A Tale of Two Cities', got {got!r}"


def test_fixes_shouting_and_odd_capitals():
    got = title_case("hARRY pOTTER AND THE chamber OF secrets", MINOR)
    want = "Harry Potter and the Chamber of Secrets"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_collapses_extra_spaces():
    got = title_case("  war   and  peace ", MINOR)
    assert got == "War and Peace", f"expected 'War and Peace', got {got!r}"


def test_empty_title_and_no_minor_words():
    assert title_case("", MINOR) == "", f"expected '', got {title_case('', MINOR)!r}"
    got = title_case("of mice and men", set())
    assert got == "Of Mice And Men", f"expected 'Of Mice And Men', got {got!r}"
