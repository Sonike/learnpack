from solution import Request, parse_request


def test_parses_a_simple_get():
    raw = "GET /tasks?status=todo HTTP/1.1\r\nHost: localhost:8000\r\nAccept: application/json\r\n\r\n"
    got = parse_request(raw)
    want = Request("GET", "/tasks", {"status": "todo"},
                   {"host": "localhost:8000", "accept": "application/json"}, "")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_parses_a_post_with_a_json_body():
    body = '{"title": "Write docs", "note": "a\\r\\nb"}'
    raw = ("POST /tasks HTTP/1.1\r\nHost: api.example.com\r\n"
           f"Content-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n{body}")
    got = parse_request(raw)
    want = Request("POST", "/tasks", {},
                   {"host": "api.example.com", "content-type": "application/json",
                    "content-length": str(len(body))}, body)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_header_names_are_lower_cased_and_values_stripped():
    raw = "GET / HTTP/1.1\r\nX-Request-ID:   abc-123  \r\nCONTENT-TYPE:text/plain\r\n\r\n"
    got = parse_request(raw).headers
    want = {"x-request-id": "abc-123", "content-type": "text/plain"}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_body_can_contain_a_blank_line():
    raw = "POST /notes HTTP/1.1\r\nHost: x\r\n\r\nline one\r\n\r\nline three"
    got = parse_request(raw).body
    want = "line one\r\n\r\nline three"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_query_with_several_and_empty_values():
    raw = "delete /tasks/7?force=true&reason= HTTP/1.1\r\nHost: x\r\n\r\n"
    got = parse_request(raw)
    assert got.method == "DELETE", f"expected 'DELETE', got {got.method!r}"
    assert got.path == "/tasks/7", f"expected '/tasks/7', got {got.path!r}"
    want = {"force": "true", "reason": ""}
    assert got.query == want, f"expected {want!r}, got {got.query!r}"
