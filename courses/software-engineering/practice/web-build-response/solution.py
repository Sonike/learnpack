import json
from http import HTTPStatus


def build_response(status: int, body: dict) -> str:
    """The full text of an HTTP/1.1 response with a JSON body."""
    text = json.dumps(body, ensure_ascii=False)
    reason = HTTPStatus(status).phrase
    return (
        f"HTTP/1.1 {status} {reason}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(text.encode('utf-8'))}\r\n"
        "\r\n"
        f"{text}"
    )


if __name__ == "__main__":
    print(repr(build_response(201, {"id": 7})))
