import csv
import io
from datetime import datetime, timezone


# Written by an AI assistant. It has three bugs. Find and fix them.
def parse_csv_dates(csv_text: str, column: str) -> list[datetime]:
    """Parse the ISO 8601 timestamps in `column` and return them in UTC."""
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    results = []
    for row in rows[1:]:  # skip the header row
        value = row[column].strip()
        if not value:
            continue
        try:
            parsed = datetime.fromisoformat(value)
            results.append(parsed.replace(tzinfo=timezone.utc))  # make it UTC
        except ValueError:
            continue  # ignore bad rows
    return results


if __name__ == "__main__":
    text = """id,created_at
1,2026-03-01T09:30:00+01:00
2,2026-03-01T12:00:00
3,
"""
    for d in parse_csv_dates(text, "created_at"):
        print(d.isoformat())
    # Expected:
    # 2026-03-01T08:30:00+00:00
    # 2026-03-01T12:00:00+00:00
