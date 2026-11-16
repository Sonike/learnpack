import csv


def load_contacts(path) -> list[dict]:
    """Read a CSV of contacts. Strip whitespace from keys and values; skip blank rows."""
    contacts = []
    # TODO: with open(path, encoding="utf-8", newline="") as f:
    #           for row in csv.DictReader(f): ...
    # TODO: build a cleaned dict: key.strip() -> (value or "").strip()
    # TODO: only keep it if at least one value is non-empty
    return contacts


if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "contacts.csv"
        path.write_text(
            "name, email ,city\n Ada , ada@example.com, London\n,,\nGrace,grace@example.com,  New York\n",
            encoding="utf-8",
        )
        for contact in load_contacts(path):
            print(contact)
