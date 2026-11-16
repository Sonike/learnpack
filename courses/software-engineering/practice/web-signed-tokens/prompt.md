# Signed login tokens with HMAC

Write `sign` and `verify`: a tiny version of the signed tokens APIs hand out after login. Anyone can read a token, but nobody without the secret can change it or make a new one.

```python
def sign(payload: dict, secret: bytes) -> str: ...
def verify(token: str, secret: bytes, now: float) -> dict | None: ...
```

### `sign(payload, secret)`

- `payload`: a dict such as `{"user_id": 7, "exp": 1_800_000_000}`. `exp` is the expiry time as a Unix timestamp (seconds).
- `secret`: the server's secret key, as bytes.
- Build the token as `<body>.<signature>`:
  - `body` = `base64.urlsafe_b64encode(json.dumps(payload, sort_keys=True).encode("utf-8")).decode("ascii")`
  - `signature` = `hmac.new(secret, body.encode("ascii"), hashlib.sha256).hexdigest()`

### `verify(token, secret, now)`

- `now`: the current time as a Unix timestamp. It's passed in (instead of calling `time.time()`) so tests can control the clock.
- Return the payload dict if **all** of these hold, otherwise return `None`:
  1. The token is exactly two parts separated by one `.`.
  2. The signature matches the body. **Compare with `hmac.compare_digest`**, not `==`. (Compare bytes, `given.encode()` vs `expected.encode()`: `compare_digest` refuses non-ASCII strings.)
  3. The body decodes to a JSON object (a dict).
  4. It has an `"exp"` and `now < exp` (a token is expired at the moment `now == exp`).
- `verify` must **never raise**, whatever junk it's given. Catch decoding errors (`ValueError` covers bad base64, bad JSON and bad UTF-8) and return `None`.

## Example

```python
token = sign({"user_id": 7, "exp": 1000}, b"s3cret")
verify(token, b"s3cret", now=999)     # {'exp': 1000, 'user_id': 7}
verify(token, b"s3cret", now=1000)    # None  (expired)
verify(token, b"wrong", now=999)      # None  (signature doesn't match)
```
