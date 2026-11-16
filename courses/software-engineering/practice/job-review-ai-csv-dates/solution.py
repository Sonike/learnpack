import csv
import io
from datetime import datetime, timezone


def parse_csv_dates(csv_text: str, column: str) -> list[datetime]:
    """Parse the ISO 8601 timestamps in `column` and return them in UTC."""
    reader = csv.DictReader(io.StringIO(csv_text))
    results = []
    # Bug 2 fixed: DictReader already used the header, so every row is data.
    # The header is line 1, so the first data row is line 2.
    for line_number, row in enumerate(reader, start=2):
        value = (row[column] or "").strip()
        if not value:
            continue
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            # Bug 3 fixed: say which line is bad instead of silently dropping it.
            raise ValueError(f"line {line_number}: bad date {value!r}") from None
        # Bug 1 fixed: convert an existing offset instead of overwriting it.
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        results.append(parsed.astimezone(timezone.utc))
    return results
