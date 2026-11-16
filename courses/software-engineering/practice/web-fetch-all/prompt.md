# Follow cursors to fetch every page

An API returns its results one page at a time. Write `fetch_all(get_page, max_pages)` that keeps asking for the next page until there are no more, and returns every item in order.

```python
def fetch_all(get_page, max_pages: int = 100) -> list[dict]: ...
```

- `get_page(cursor)` makes one request and returns a dict like:
  ```python
  {"items": [{"id": 1}, {"id": 2}], "next_cursor": "abc"}
  ```
  Call it with `None` for the first page, then with each `next_cursor` you receive. When `next_cursor` is `None`, you've reached the last page.
  (In real code `get_page` would make an HTTP request. Here it's passed in, so tests can give you a fake API with no network.)
- `max_pages` is a safety limit. If you've fetched `max_pages` pages and there's **still** a next cursor, raise `RuntimeError` instead of looping forever (a buggy API might return the same cursor again and again).
- Call `get_page` once per page, no more.

## Example

```python
PAGES = {
    None: {"items": [{"id": 1}, {"id": 2}], "next_cursor": "p2"},
    "p2": {"items": [{"id": 3}], "next_cursor": None},
}
fetch_all(lambda cursor: PAGES[cursor])
# [{'id': 1}, {'id': 2}, {'id': 3}]
```
