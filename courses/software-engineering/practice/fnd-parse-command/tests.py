from solution import parse_command


def test_command_with_one_flag_and_one_argument():
    got = parse_command("ls -la projects")
    want = ("ls", ["-la"], ["projects"])
    assert got == want, f"expected {want!r}, got {got!r}"


def test_command_on_its_own():
    got = parse_command("pwd")
    want = ("pwd", [], [])
    assert got == want, f"expected {want!r}, got {got!r}"


def test_quoted_path_with_spaces_is_one_argument():
    got = parse_command('cp -r "My Documents" backup --verbose')
    want = ("cp", ["-r", "--verbose"], ["My Documents", "backup"])
    assert got == want, f"expected {want!r}, got {got!r}"


def test_single_quotes_and_extra_spaces():
    got = parse_command("  grep   -i  'hello world'   notes.txt  ")
    want = ("grep", ["-i"], ["hello world", "notes.txt"])
    assert got == want, f"expected {want!r}, got {got!r}"


def test_blank_line_gives_empty_parts():
    for line in ["", "   "]:
        got = parse_command(line)
        assert got == ("", [], []), f"parse_command({line!r}): expected ('', [], []), got {got!r}"
