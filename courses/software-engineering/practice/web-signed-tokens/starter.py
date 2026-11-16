import base64
import hashlib
import hmac
import json


def sign(payload: dict, secret: bytes) -> str:
    """'<base64 JSON body>.<hex HMAC-SHA256 of the body>'"""
    # TODO: body = urlsafe base64 of the sorted JSON; signature = HMAC-SHA256 hexdigest of body
    return ""


def verify(token: str, secret: bytes, now: float) -> dict | None:
    """The payload if the token is genuine and not expired, else None. Never raises."""
    # TODO 1: split into body and signature (exactly one '.')
    # TODO 2: recompute the signature and compare with hmac.compare_digest
    # TODO 3: decode the body (catch ValueError) and check it's a dict
    # TODO 4: check "exp" exists and now < exp
    return None


if __name__ == "__main__":
    token = sign({"user_id": 7, "exp": 1000}, b"s3cret")
    print(token)
    print(verify(token, b"s3cret", now=999))
    print(verify(token, b"s3cret", now=1000))
    print(verify(token, b"wrong", now=999))
