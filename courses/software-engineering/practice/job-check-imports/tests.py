from solution import check_imports


def test_standard_library_imports_are_fine():
    got = check_imports("import os\nimport json, csv\nfrom pathlib import Path\n", set())
    assert got == [], f"expected [], got {got!r}"


def test_approved_packages_are_fine():
    got = check_imports("import fastapi\nfrom pydantic import BaseModel\n", {"fastapi", "pydantic"})
    assert got == [], f"expected [], got {got!r}"


def test_flags_unknown_packages_sorted():
    got = check_imports("import requestz\nimport fastapi_auth_magic\nimport os\n", set())
    want = ["fastapi_auth_magic", "requestz"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_uses_top_level_name_of_dotted_imports():
    got = check_imports("import sklearn.metrics\nfrom sklearn.model_selection import split\nimport os.path\n", set())
    assert got == ["sklearn"], f"expected ['sklearn'], got {got!r}"


def test_ignores_relative_imports():
    got = check_imports("from . import helpers\nfrom .models import User\nfrom ..db import conn\n", set())
    assert got == [], f"expected [], got {got!r}"


def test_ignores_imports_inside_strings_and_comments():
    code = 'text = "import totally_fake"\n# import also_fake\nimport math\n'
    got = check_imports(code, set())
    assert got == [], f"expected [], got {got!r}"
