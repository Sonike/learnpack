import json
from http import HTTPStatus


def build_response(status: int, body: dict) -> str:
    """The full text of an HTTP/1.1 response with a JSON body."""
    # TODO 1: encode body with json.dumps(body, ensure_ascii=False)
    # TODO 2: status line "HTTP/1.1 <code> <reason>" (HTTPStatus(status).phrase)
    # TODO 3: Content-Type and Content-Length (in BYTES), a blank line, then the body
    return ""


if __name__ == "__main__":
    print(repr(build_response(201, {"id": 7})))
    print(build_response(200, {"city": "Abéòkúta"}))
