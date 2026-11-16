import base64
import hashlib
import hmac
import json


def _signature(body: str, secret: bytes) -> str:
    return hmac.new(secret, body.encode("ascii"), hashlib.sha256).hexdigest()


def sign(payload: dict, secret: bytes) -> str:
    """'<base64 JSON body>.<hex HMAC-SHA256 of the body>'"""
    body = base64.urlsafe_b64encode(json.dumps(payload, sort_keys=True).encode("utf-8")).decode("ascii")
    return f"{body}.{_signature(body, secret)}"


def verify(token: str, secret: bytes, now: float) -> dict | None:
    """The payload if the token is genuine and not expired, else None. Never raises."""
    parts = token.split(".")
    if len(parts) != 2:
        return None
    body, given = parts
    try:
        expected = _signature(body, secret)
    except UnicodeEncodeError:  # non-ASCII junk can't be a body we made
        return None
    if not hmac.compare_digest(given.encode("utf-8"), expected.encode("ascii")):
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(body.encode("ascii")))
    except ValueError:  # bad base64, bad UTF-8 and bad JSON are all ValueErrors
        return None
    if not isinstance(payload, dict) or "exp" not in payload:
        return None
    if not now < payload["exp"]:
        return None
    return payload


if __name__ == "__main__":
    token = sign({"user_id": 7, "exp": 1000}, b"s3cret")
    print(verify(token, b"s3cret", now=999))
