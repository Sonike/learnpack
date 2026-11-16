def fetch_all(get_page, max_pages: int = 100) -> list[dict]:
    """Every item from every page, following next_cursor until it is None."""
    # TODO: start with cursor None, collect items, follow next_cursor,
    #       and raise RuntimeError if max_pages pages weren't enough
    return []


if __name__ == "__main__":
    PAGES = {
        None: {"items": [{"id": 1}, {"id": 2}], "next_cursor": "p2"},
        "p2": {"items": [{"id": 3}], "next_cursor": None},
    }
    print(fetch_all(lambda cursor: PAGES[cursor]))
