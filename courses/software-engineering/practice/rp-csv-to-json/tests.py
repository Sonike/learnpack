import json
import tempfile
from pathlib import Path

from solution import csv_to_json


def convert(csv_text):
    """Run csv_to_json on csv_text; return (count, parsed JSON, raw JSON text)."""
    with tempfile.TemporaryDirectory() as folder:
        src = Path(folder) / "in.csv"
        dst = Path(folder) / "out.json"
        src.write_text(csv_text, encoding="utf-8")
        count = csv_to_json(src, dst)
        raw = dst.read_text(encoding="utf-8")
    return count, json.loads(raw), raw


def test_returns_the_row_count():
    count, _, _ = convert("name,age\nAda,36\nGrace,45\nLinus,28\n")
    assert count == 3, f"expected 3, got {count!r}"


def test_writes_a_list_of_objects_in_order():
    _, data, _ = convert("name,age\nAda,36\nGrace,45\n")
    want = [{"name": "Ada", "age": "36"}, {"name": "Grace", "age": "45"}]
    assert data == want, f"expected {want!r}, got {data!r}"


def test_keeps_non_english_text_readable():
    _, data, raw = convert("name,city\nZoë,Kraków\n")
    assert data == [{"name": "Zoë", "city": "Kraków"}], f"got {data!r}"
    assert "Zoë" in raw, "use ensure_ascii=False so the file shows Zoë, not \\u00eb"


def test_quoted_commas_stay_in_one_value():
    _, data, _ = convert('name,address\nAda,"12 High St, London"\n')
    want = [{"name": "Ada", "address": "12 High St, London"}]
    assert data == want, f"expected {want!r}, got {data!r}"


def test_header_only_csv_writes_an_empty_list():
    count, data, _ = convert("name,age\n")
    assert count == 0, f"expected 0, got {count!r}"
    assert data == [], f"expected [], got {data!r}"
