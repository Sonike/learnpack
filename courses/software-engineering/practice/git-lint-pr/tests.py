from solution import lint_pr_description

GOOD = """## What
Add a password reset email.

## Why
Users locked out of their accounts had to email support. Closes #42.

## How to test
1. Run `pytest tests/test_reset.py`
2. Request a reset for a test account and open the link.

Size: 180 lines
"""


def test_a_complete_description_has_no_problems():
    got = lint_pr_description(GOOD)
    assert got == [], f"expected [], got {got!r}"


def test_reports_every_problem_in_order():
    got = lint_pr_description("Fixed stuff\n\nSize: 950")
    want = [
        "Missing section: What",
        "Missing section: Why",
        "Missing section: How to test",
        "No linked issue (add e.g. Closes #123)",
        "Too big: 950 changed lines (aim for under 400)",
    ]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_headings_ignore_case_level_and_a_trailing_colon():
    md = "# what\nx\n### WHY:\ny, see #7\n## How to test:\nrun it\n"
    got = lint_pr_description(md)
    assert got == [], f"expected [], got {got!r}"


def test_a_word_in_the_text_is_not_a_heading():
    md = "What I did: lots.\nWhy: because.\n## How to test\nRun it. Fixes #3"
    got = lint_pr_description(md)
    want = ["Missing section: What", "Missing section: Why"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_missing_issue_link_is_reported():
    md = GOOD.replace("Closes #42.", "")
    got = lint_pr_description(md)
    want = ["No linked issue (add e.g. Closes #123)"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_size_limit_is_over_400_not_at_400():
    assert lint_pr_description(GOOD.replace("Size: 180", "Size: 400")) == [], "400 lines is allowed"
    got = lint_pr_description(GOOD.replace("Size: 180", "size: 401"))
    want = ["Too big: 401 changed lines (aim for under 400)"]
    assert got == want, f"expected {want!r}, got {got!r}"
