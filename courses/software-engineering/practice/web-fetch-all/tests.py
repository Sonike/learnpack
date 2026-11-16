from solution import fetch_all


class FakeApi:
    """Serves pages from a dict and records every cursor it was asked for."""

    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def __call__(self, cursor):
        self.calls.append(cursor)
        return self.pages[cursor]


def test_collects_items_from_every_page_in_order():
    api = FakeApi({
        None: {"items": [{"id": 1}, {"id": 2}], "next_cursor": "p2"},
        "p2": {"items": [{"id": 3}], "next_cursor": "p3"},
        "p3": {"items": [{"id": 4}, {"id": 5}], "next_cursor": None},
    })
    got = fetch_all(api)
    want = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_calls_the_api_once_per_page_with_each_cursor():
    api = FakeApi({
        None: {"items": [{"id": 1}], "next_cursor": "p2"},
        "p2": {"items": [{"id": 2}], "next_cursor": None},
    })
    fetch_all(api)
    want = [None, "p2"]
    assert api.calls == want, f"expected calls {want!r}, got {api.calls!r}"


def test_single_empty_page():
    api = FakeApi({None: {"items": [], "next_cursor": None}})
    got = fetch_all(api)
    assert got == [], f"expected {[]!r}, got {got!r}"


def test_stops_with_runtime_error_when_the_cursor_never_ends():
    api = FakeApi({None: {"items": [{"id": 1}], "next_cursor": "same"},
                   "same": {"items": [{"id": 1}], "next_cursor": "same"}})
    try:
        fetch_all(api, max_pages=5)
        raised = False
    except RuntimeError:
        raised = True
    assert raised, "expected RuntimeError when pages never end"
    assert len(api.calls) == 5, f"expected exactly 5 calls, got {len(api.calls)}"


def test_exactly_max_pages_is_fine():
    api = FakeApi({
        None: {"items": [{"id": 1}], "next_cursor": "p2"},
        "p2": {"items": [{"id": 2}], "next_cursor": None},
    })
    got = fetch_all(api, max_pages=2)
    want = [{"id": 1}, {"id": 2}]
    assert got == want, f"expected {want!r}, got {got!r}"
