from solution import build_response


def test_builds_a_201_response():
    got = build_response(201, {"id": 7})
    want = 'HTTP/1.1 201 Created\r\nContent-Type: application/json\r\nContent-Length: 9\r\n\r\n{"id": 7}'
    assert got == want, f"expected {want!r}, got {got!r}"


def test_uses_the_right_reason_phrase():
    for status, reason in [(200, "OK"), (404, "Not Found"), (409, "Conflict"), (500, "Internal Server Error")]:
        got = build_response(status, {}).split("\r\n")[0]
        want = f"HTTP/1.1 {status} {reason}"
        assert got == want, f"expected {want!r}, got {got!r}"


def test_content_length_counts_bytes_not_characters():
    got = build_response(200, {"city": "Abéòkúta"})
    body = '{"city": "Abéòkúta"}'
    want = f"Content-Length: {len(body.encode('utf-8'))}"  # 23 bytes, 20 characters
    assert want in got, f"expected the header {want!r} in {got!r}"
    assert got.endswith(body), f"expected the body {body!r} with real characters, got {got!r}"


def test_empty_body_dict():
    got = build_response(200, {})
    want = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 2\r\n\r\n{}"
    assert got == want, f"expected {want!r}, got {got!r}"
