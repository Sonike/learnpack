import csv
import json


def csv_to_json(csv_path, json_path) -> int:
    """Write the CSV's rows to json_path as a list of objects. Return the row count."""
    rows = []
    # TODO: read the CSV with csv.DictReader into rows (a list of dicts)
    # TODO: write rows to json_path with json.dump(rows, f, indent=2, ensure_ascii=False)
    return len(rows)


if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as folder:
        src = Path(folder) / "people.csv"
        dst = Path(folder) / "people.json"
        src.write_text("name,age\nAda,36\nZoë,29\n", encoding="utf-8")
        print("rows:", csv_to_json(src, dst))
        if dst.exists():
            print(dst.read_text(encoding="utf-8"))
