import csv


def load_contacts(path) -> list[dict]:
    """Read a CSV of contacts. Strip whitespace from keys and values; skip blank rows."""
    contacts = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            cleaned = {key.strip(): (value or "").strip() for key, value in row.items()}
            if any(cleaned.values()):
                contacts.append(cleaned)
    return contacts
