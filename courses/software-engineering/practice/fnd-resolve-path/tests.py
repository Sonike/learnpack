import posixpath

from solution import resolve


def expected(cwd, path):
    return posixpath.normpath(posixpath.join(cwd, path))


def test_relative_path_is_joined_to_cwd():
    got = resolve("/home/ada", "projects/app")
    assert got == "/home/ada/projects/app", f"expected '/home/ada/projects/app', got {got!r}"


def test_dot_dot_goes_up_one_folder():
    got = resolve("/home/ada/projects", "../data/file.csv")
    assert got == "/home/ada/data/file.csv", f"expected '/home/ada/data/file.csv', got {got!r}"


def test_absolute_path_ignores_cwd():
    got = resolve("/home/ada", "/etc//hosts/")
    assert got == "/etc/hosts", f"expected '/etc/hosts', got {got!r}"


def test_cannot_go_above_the_root():
    for cwd, path in [("/", ".."), ("/", "../.."), ("/tmp", "../../../x")]:
        want = expected(cwd, path)
        got = resolve(cwd, path)
        assert got == want, f"resolve({cwd!r}, {path!r}): expected {want!r}, got {got!r}"


def test_dots_and_empty_path_stay_in_cwd():
    for path in ["", ".", "./", "./."]:
        got = resolve("/home/ada", path)
        assert got == "/home/ada", f"resolve('/home/ada', {path!r}): expected '/home/ada', got {got!r}"


def test_matches_posixpath_on_mixed_cases():
    cases = [
        ("/a/b/c", "../../d"),
        ("/a/b", "./c/../d/./e"),
        ("/a", "b//c///d/"),
        ("/a/b", "../b/../b/c"),
        ("/", "x/y/.."),
    ]
    for cwd, path in cases:
        want = expected(cwd, path)
        got = resolve(cwd, path)
        assert got == want, f"resolve({cwd!r}, {path!r}): expected {want!r}, got {got!r}"
