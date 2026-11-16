import csv
import json


def csv_to_json(csv_path, json_path) -> int:
    """Write the CSV's rows to json_path as a list of objects. Return the row count."""
    with open(csv_path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    return len(rows)
