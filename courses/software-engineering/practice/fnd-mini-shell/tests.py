from solution import run


def test_starts_at_the_root():
    got = run(["pwd", "ls"])
    assert got == ["/"], f"expected ['/'], got {got!r}"


def test_mkdir_and_ls_sorted():
    got = run(["mkdir notes", "mkdir code", "mkdir art", "ls"])
    assert got == ["art", "code", "notes"], f"expected ['art', 'code', 'notes'], got {got!r}"


def test_cd_into_nested_folders_and_back():
    got = run(["mkdir a", "cd a", "mkdir b", "cd b", "pwd", "cd ..", "pwd", "cd /", "pwd"])
    assert got == ["/a/b", "/a", "/"], f"expected ['/a/b', '/a', '/'], got {got!r}"


def test_cd_into_missing_folder_reports_error_and_stays_put():
    got = run(["mkdir notes", "cd music", "pwd"])
    want = ["cd: no such file or directory: music", "/"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_mkdir_existing_folder_and_unknown_command():
    got = run(["mkdir notes", "mkdir notes", "rm notes", "ls"])
    want = ["mkdir: notes: File exists", "command not found: rm", "notes"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_folders_with_same_name_in_different_places_are_separate():
    got = run(["mkdir a", "mkdir b", "cd a", "mkdir x", "cd ..", "cd b", "ls", "cd ..", "cd ..", "pwd", "ls"])
    want = ["/", "a", "b"]
    assert got == want, f"expected {want!r} (b is empty; cd .. at / stays at /), got {got!r}"
