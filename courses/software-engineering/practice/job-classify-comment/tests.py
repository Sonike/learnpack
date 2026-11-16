from solution import classify_comment


def check(text, want):
    got = classify_comment(text)
    assert got == want, f"expected {want!r} for {text!r}, got {got!r}"


def test_reads_conventional_prefixes():
    check("nit: extra blank line here", "nit")
    check("nitpick: prefer f-strings", "nit")
    check("praise: great test names", "praise")
    check("issue: this crashes on empty input", "blocking")


def test_prefix_is_case_insensitive():
    check("Question: why a list and not a set?", "question")
    check("NIT : trailing space", "nit")


def test_prefix_wins_over_other_rules():
    check("nit: could this be shorter?", "nit")
    check("blocking: nice idea but this leaks the token", "blocking")


def test_trailing_question_mark_is_a_question():
    check("What happens if items is empty?", "question")


def test_praise_words_are_praise():
    check("Love how small this function is!", "praise")
    check("Thanks for adding the regression test.", "praise")


def test_unlabelled_comment_is_blocking():
    check("This query is open to SQL injection.", "blocking")
    check("Note: see the docs for retries", "blocking")
    check("Cleanup the imports", "blocking")
