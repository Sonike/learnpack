import base64
import hashlib
import hmac
import json

from solution import sign, verify

SECRET = b"test-secret"


def test_a_signed_token_verifies_before_expiry():
    payload = {"user_id": 7, "role": "member", "exp": 1000}
    got = verify(sign(payload, SECRET), SECRET, now=999)
    assert got == payload, f"expected {payload!r}, got {got!r}"


def test_token_format_is_body_dot_signature():
    token = sign({"exp": 5, "user_id": 1}, SECRET)
    body = base64.urlsafe_b64encode(json.dumps({"exp": 5, "user_id": 1}, sort_keys=True).encode()).decode()
    want = body + "." + hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest()
    assert token == want, f"expected {want!r}, got {token!r}"


def test_expired_tokens_are_rejected():
    token = sign({"user_id": 7, "exp": 1000}, SECRET)
    for now in (1000, 5000):
        got = verify(token, SECRET, now=now)
        assert got is None, f"now={now}: expected None, got {got!r}"


def test_tampered_payload_is_rejected():
    token = sign({"user_id": 7, "exp": 1000}, SECRET)
    _, sig = token.split(".")
    forged_body = base64.urlsafe_b64encode(json.dumps({"exp": 1000, "user_id": 1}, sort_keys=True).encode()).decode()
    got = verify(forged_body + "." + sig, SECRET, now=1)
    assert got is None, f"a token with a changed user_id was accepted: {got!r}"


def test_tampered_signature_or_wrong_secret_is_rejected():
    token = sign({"user_id": 7, "exp": 1000}, SECRET)
    flipped = token[:-1] + ("0" if token[-1] != "0" else "1")
    assert verify(flipped, SECRET, now=1) is None, "a changed signature was accepted"
    assert verify(token, b"another-secret", now=1) is None, "a token was accepted with the wrong secret"


def test_junk_and_missing_exp_return_none_without_raising():
    junk = ["", "abc", "a.b.c", "!!!.sig", "é.é", "abc.é", sign({"user_id": 7}, SECRET), sign([1, 2], SECRET)]
    body = "not*base64"
    junk.append(body + "." + hmac.new(SECRET, body.encode(), hashlib.sha256).hexdigest())
    for token in junk:
        got = verify(token, SECRET, now=1)
        assert got is None, f"{token!r}: expected None, got {got!r}"
