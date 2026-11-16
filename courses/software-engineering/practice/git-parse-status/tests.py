from solution import parse_status_porcelain


def test_staged_modified_and_untracked_files():
    got = parse_status_porcelain("M  app.py\n M README.md\n?? notes.txt\n")
    want = {"staged": ["app.py"], "modified": ["README.md"], "untracked": ["notes.txt"]}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_file_staged_then_edited_again_is_in_both_lists():
    got = parse_status_porcelain("MM utils.py\n")
    want = {"staged": ["utils.py"], "modified": ["utils.py"], "untracked": []}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_added_deleted_and_renamed_files():
    text = "A  tests/test_app.py\nD  old.txt\n D gone.py\nR  old_name.py -> new_name.py\n"
    got = parse_status_porcelain(text)
    want = {"staged": ["tests/test_app.py", "old.txt", "new_name.py"], "modified": ["gone.py"], "untracked": []}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_clean_repo_gives_three_empty_lists():
    got = parse_status_porcelain("")
    want = {"staged": [], "modified": [], "untracked": []}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_skips_blank_lines_and_ignored_files():
    got = parse_status_porcelain("\n!! .venv/\n?? src/new_module.py\n\n")
    want = {"staged": [], "modified": [], "untracked": ["src/new_module.py"]}
    assert got == want, f"expected {want!r}, got {got!r}"
