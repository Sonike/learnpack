def sort_students(records: list[dict]) -> list[dict]:
    """New list: highest grade first, then name A-Z. Doesn't change records."""
    return sorted(records, key=lambda r: (-r["grade"], r["name"]))
