from solution import check_pyproject

GOOD = '''
[project]
name = "habit-api"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "uvicorn~=0.30"]

[dependency-groups]
dev = ["pytest>=8", "ruff>=0.6"]
'''


def test_a_good_file_has_no_problems():
    got = check_pyproject(GOOD)
    want = []
    assert got == want, f"expected {want!r}, got {got!r}"


def test_reports_all_problems_in_order():
    text = '''
[project]
name = "habit-api"
dependencies = ["fastapi>=0.115", "requests", " httpx "]

[dependency-groups]
dev = ["ruff>=0.6"]
'''
    got = check_pyproject(text)
    want = [
        "missing requires-python",
        "unpinned dependency: requests",
        "unpinned dependency: httpx",
        "missing test dependency (pytest)",
    ]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_finds_pytest_in_optional_dependencies_with_extras():
    text = '''
[project]
name = "x"
requires-python = ">=3.12"

[project.optional-dependencies]
test = ["PyTest[testing]>=8"]
'''
    got = check_pyproject(text)
    want = []
    assert got == want, f"expected {want!r}, got {got!r}"


def test_pytest_lookalike_does_not_count():
    text = GOOD.replace('"pytest>=8"', '"pytest-cov>=5"')
    got = check_pyproject(text)
    want = ["missing test dependency (pytest)"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_invalid_toml_and_missing_project_table():
    got = (check_pyproject('[project\nname = "x"'), check_pyproject('[tool.ruff]\nline-length = 100'))
    want = (["invalid TOML"], ["missing [project] table"])
    assert got == want, f"expected {want!r}, got {got!r}"
