def sort_students(records: list[dict]) -> list[dict]:
    """New list: highest grade first, then name A-Z. Doesn't change records."""
    # TODO: return sorted(records, key=lambda r: ...)
    return list(records)


if __name__ == "__main__":
    students = [
        {"name": "Grace", "grade": 85},
        {"name": "Ada", "grade": 91},
        {"name": "Alan", "grade": 85},
    ]
    for s in sort_students(students):
        print(s)
