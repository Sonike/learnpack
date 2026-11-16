from dataclasses import dataclass
from urllib.parse import parse_qsl


@dataclass
class Request:
    method: str
    path: str
    query: dict[str, str]
    headers: dict[str, str]
    body: str


def parse_request(raw: str) -> Request:
    """Turn a raw HTTP/1.1 request string into a Request."""
    head, _, body = raw.partition("\r\n\r\n")
    request_line, *header_lines = head.split("\r\n")
    method, target, _version = request_line.split(" ")
    path, _, query_string = target.partition("?")

    headers = {}
    for line in header_lines:
        if line:
            name, _, value = line.partition(":")
            headers[name.strip().lower()] = value.strip()

    query = dict(parse_qsl(query_string, keep_blank_values=True))
    return Request(method.upper(), path, query, headers, body)


if __name__ == "__main__":
    raw = "GET /tasks?status=todo HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
    print(parse_request(raw))
