from solution import check_commit_message

IMPERATIVE = 'Use the imperative mood ("Fix bug", not "Fixed bug")'


def test_a_good_message_has_no_problems():
    msg = (
        "Add password reset email\n"
        "\n"
        "Users who forgot their password had to email support, which took a\n"
        "day on average. Send a one-time reset link instead.\n"
    )
    got = check_commit_message(msg)
    assert got == [], f"expected [], got {got!r}"


def test_a_bad_subject_reports_every_problem_in_order():
    got = check_commit_message("fixed the login bug that happened when the password was empty.")
    want = [
        "Subject is 62 characters (keep it to 50)",
        "Capitalize the subject line",
        "Do not end the subject with a period",
        IMPERATIVE,
    ]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_imperative_heuristic_and_its_exceptions():
    assert check_commit_message("Fixing flaky test") == [IMPERATIVE], "'Fixing' is not imperative"
    assert check_commit_message("Updated README") == [IMPERATIVE], "'Updated' is not imperative"
    for ok in ["Fix flaky test", "Embed the logo in the PDF", "Bring back the dark theme", "Speed up search"]:
        got = check_commit_message(ok)
        assert got == [], f"{ok!r} is imperative: expected [], got {got!r}"


def test_body_needs_a_blank_line_and_wrapping_at_72():
    long_line = "x" * 80
    got = check_commit_message(f"Add caching\nIt was slow.\n{long_line}\n")
    want = ["Separate subject from body with a blank line", "Body line 3 is 80 characters (wrap at 72)"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_comment_lines_and_trailing_blank_lines_are_ignored():
    msg = "Add caching\n\n# Please enter the commit message for your changes.\n# " + "x" * 90 + "\n\n\n"
    got = check_commit_message(msg)
    assert got == [], f"expected [], got {got!r}"


def test_empty_message():
    for msg in ["", "\n\n", "# only a comment\n"]:
        got = check_commit_message(msg)
        assert got == ["Message is empty"], f"for {msg!r}: expected ['Message is empty'], got {got!r}"


def test_exactly_50_characters_is_fine():
    subject = "Add " + "a" * 46
    got = check_commit_message(subject)
    assert got == [], f"a 50-character subject is allowed, got {got!r}"
