import tempfile
from pathlib import Path

from solution import load_contacts


def write_csv(folder, text):
    path = Path(folder) / "contacts.csv"
    path.write_text(text, encoding="utf-8")
    return path


def test_reads_rows_as_dicts():
    with tempfile.TemporaryDirectory() as folder:
        path = write_csv(folder, "name,email\nAda,ada@example.com\nGrace,grace@example.com\n")
        got = load_contacts(path)
    want = [{"name": "Ada", "email": "ada@example.com"}, {"name": "Grace", "email": "grace@example.com"}]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_strips_whitespace_from_keys_and_values():
    with tempfile.TemporaryDirectory() as folder:
        path = write_csv(folder, "name, email ,city\n Ada , ada@example.com,  London \n")
        got = load_contacts(path)
    want = [{"name": "Ada", "email": "ada@example.com", "city": "London"}]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_skips_blank_rows():
    with tempfile.TemporaryDirectory() as folder:
        path = write_csv(folder, "name,email\n,\nAda,ada@example.com\n\n  ,  \n")
        got = load_contacts(path)
    want = [{"name": "Ada", "email": "ada@example.com"}]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_short_rows_get_empty_strings():
    with tempfile.TemporaryDirectory() as folder:
        path = write_csv(folder, "name,email,city\nAda,ada@example.com\n")
        got = load_contacts(path)
    want = [{"name": "Ada", "email": "ada@example.com", "city": ""}]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_reads_non_english_names_and_accepts_a_string_path():
    with tempfile.TemporaryDirectory() as folder:
        path = write_csv(folder, "name,city\nZoë,Kraków\nChidi,Enugu\n")
        got = load_contacts(str(path))
    want = [{"name": "Zoë", "city": "Kraków"}, {"name": "Chidi", "city": "Enugu"}]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_header_only_file_gives_an_empty_list():
    with tempfile.TemporaryDirectory() as folder:
        path = write_csv(folder, "name,email\n")
        got = load_contacts(path)
    assert got == [], f"expected [], got {got!r}"
