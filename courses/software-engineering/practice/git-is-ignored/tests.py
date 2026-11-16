from solution import is_ignored

PYTHON_GITIGNORE = ["# Python", "__pycache__/", "*.pyc", ".venv/", ".env", "", "*.log", "!keep.log"]


def test_ignores_files_by_extension_anywhere():
    for path in ["app.pyc", "src/models/user.pyc"]:
        assert is_ignored(path, PYTHON_GITIGNORE), f"{path!r} should be ignored by *.pyc"


def test_folder_patterns_ignore_everything_inside():
    for path in [".venv/bin/python", "src/__pycache__/app.cpython-312.pyc"]:
        assert is_ignored(path, PYTHON_GITIGNORE), f"{path!r} is inside an ignored folder"


def test_folder_patterns_do_not_match_files_with_that_name():
    assert not is_ignored("build", ["build/"]), "'build/' only matches folders, and here build is a file"
    assert is_ignored("build/out.txt", ["build/"]), "'build/out.txt' is inside the build folder"


def test_last_matching_pattern_wins_and_negation_unignores():
    assert is_ignored("server.log", PYTHON_GITIGNORE), "server.log matches *.log"
    assert not is_ignored("keep.log", PYTHON_GITIGNORE), "!keep.log comes after *.log, so it wins"
    assert is_ignored("keep.log", ["!keep.log", "*.log"]), "here *.log comes last, so it wins"


def test_patterns_with_a_slash_match_the_whole_path():
    patterns = ["docs/*.md", "/config.ini"]
    assert is_ignored("docs/notes.md", patterns), "docs/notes.md matches docs/*.md"
    assert not is_ignored("notes.md", patterns), "notes.md is not under docs/"
    assert is_ignored("config.ini", patterns), "a leading / anchors the pattern to the repo root"
    assert not is_ignored("app/config.ini", patterns), "/config.ini only matches at the root"


def test_normal_source_files_are_not_ignored():
    for path in ["app/main.py", "README.md", ".gitignore", "tests/test_app.py"]:
        assert not is_ignored(path, PYTHON_GITIGNORE), f"{path!r} should be tracked"
    assert not is_ignored("main.py", []), "no patterns means nothing is ignored"
