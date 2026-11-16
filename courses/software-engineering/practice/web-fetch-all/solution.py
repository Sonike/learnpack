def fetch_all(get_page, max_pages: int = 100) -> list[dict]:
    """Every item from every page, following next_cursor until it is None."""
    items = []
    cursor = None
    for _ in range(max_pages):
        page = get_page(cursor)
        items.extend(page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            return items
    raise RuntimeError(f"still more pages after {max_pages}; stopping")


if __name__ == "__main__":
    PAGES = {
        None: {"items": [{"id": 1}, {"id": 2}], "next_cursor": "p2"},
        "p2": {"items": [{"id": 3}], "next_cursor": None},
    }
    print(fetch_all(lambda cursor: PAGES[cursor]))
