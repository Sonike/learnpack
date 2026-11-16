from pathlib import PurePosixPath

from solution import split_name


def expected(name):
    p = PurePosixPath(name)
    return (p.stem, p.suffix)


def test_simple_extension():
    got = split_name("photo.jpg")
    assert got == ("photo", ".jpg"), f"expected ('photo', '.jpg'), got {got!r}"


def test_only_the_last_dot_counts():
    got = split_name("archive.tar.gz")
    assert got == ("archive.tar", ".gz"), f"expected ('archive.tar', '.gz'), got {got!r}"


def test_no_extension():
    got = split_name("Makefile")
    assert got == ("Makefile", ""), f"expected ('Makefile', ''), got {got!r}"


def test_hidden_file_has_no_extension():
    got = split_name(".bashrc")
    assert got == (".bashrc", ""), f"expected ('.bashrc', ''), got {got!r}"


def test_matches_pathlib_on_tricky_names():
    for name in [".env.local", "my report.final.docx", "v1.2.3", "a.b", "data.CSV"]:
        want = expected(name)
        got = split_name(name)
        assert got == want, f"split_name({name!r}): expected {want!r}, got {got!r}"
