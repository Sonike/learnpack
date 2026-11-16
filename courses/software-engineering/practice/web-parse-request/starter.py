from dataclasses import dataclass


@dataclass
class Request:
    method: str
    path: str
    query: dict[str, str]
    headers: dict[str, str]
    body: str


def parse_request(raw: str) -> Request:
    """Turn a raw HTTP/1.1 request string into a Request."""
    # TODO 1: split the head from the body at the first "\r\n\r\n"
    # TODO 2: split the head into lines; the first is the request line
    # TODO 3: METHOD TARGET VERSION -> method, and path/query from the target
    # TODO 4: each other line is "Name: value" -> lower-cased name, stripped value
    return Request("", "", {}, {}, "")


if __name__ == "__main__":
    raw = (
        "POST /tasks?draft=yes HTTP/1.1\r\n"
        "Host: localhost:8000\r\n"
        "Content-Type: application/json\r\n"
        "\r\n"
        '{"title": "Write docs"}'
    )
    print(parse_request(raw))
