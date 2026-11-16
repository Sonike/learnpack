# Auth and security basics

## Why this matters

The moment your API stores something that belongs to someone, two questions come with every request: *who is this?* and *are they allowed to do this?* Get them wrong and one user reads another's private notes, or a database leak exposes everyone's password. Security is a huge field, but a small set of habits prevents most real-world breaches, and interviewers expect juniors to know them. This lesson covers those habits, and the reasoning behind them, so you can apply them in code you haven't seen before.

## 1. Authentication vs authorisation

Two words that sound alike and mean different things:

- **Authentication** ("authn"): proving **who you are**. Logging in with a password, sending a valid token.
- **Authorisation** ("authz"): deciding **what you're allowed to do**. Can this user edit this note? Delete this account?

They happen in that order: first find out who the user is, then check what they may do. They map onto the two status codes from *HTTP in depth*:

```
No credentials, or bad ones          -> 401 Unauthorized   ("who are you?")
Known user, but not allowed          -> 403 Forbidden      ("I know you, and no")
```

(The name "401 Unauthorized" is a historical mix-up; it really means unauthenticated.)

## 2. Never store plain passwords

Suppose your `users` table stores passwords as typed:

```
id | email            | password
 1 | ada@example.com  | sunshine2026
```

Databases leak: a backup left public, an SQL injection bug, a stolen laptop. When this one leaks, the attacker has every password, and since people reuse passwords, they can now log into your users' email and bank accounts too.

So you store a **hash** instead. A **hash function** turns any input into a fixed-size fingerprint, and you can't run it backwards:

```python
import hashlib

print(hashlib.sha256(b"sunshine2026").hexdigest())
# a 64-character hex string; the same input always gives the same output
```

To check a login, hash what the user typed and compare it with the stored hash. You never need the original password.

### Why plain SHA-256 still isn't enough

SHA-256 is designed to be **fast**: a modern graphics card computes billions per second. An attacker with your leaked hashes simply hashes every common password and every word in a dictionary and looks for matches. And since `sunshine2026` always gives the same hash, every user with that password is cracked at once.

Password storage needs two more things:

1. A **salt**: a random value generated for each user and stored next to their hash. The hash is computed from salt + password, so two users with the same password get different hashes, and precomputed tables are useless.
2. A **slow** hash: an algorithm designed to take, say, a tenth of a second and lots of memory per guess. That's nothing for one login, and ruinous for someone trying billions of guesses.

The algorithms built for this are **Argon2** (the current first choice), **scrypt** and **bcrypt**. Don't implement them yourself; use a well-known library, which also handles the salt and stores everything in one string:

```python
# pip install argon2-cffi
from argon2 import PasswordHasher

ph = PasswordHasher()
stored = ph.hash("sunshine2026")
print(stored)
# $argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>   (different every time: new salt)

ph.verify(stored, "sunshine2026")    # returns True
ph.verify(stored, "wrong")           # raises argon2.exceptions.VerifyMismatchError
```

> **Note:** the practice exercises can't use these libraries (they're not in the standard library, and the browser version can't run them), so the exercises focus on signing tokens instead. In your projects, use `argon2-cffi` or `bcrypt`.

## 3. Sessions and tokens

HTTP is stateless, so after logging in, the client must prove who it is on **every** request. Two common designs:

**Server-side sessions.** On login, the server creates a random session id, stores `session_id → user_id` in a table (or a cache like Redis), and sends the id in a cookie. Each request's cookie is looked up. Easy to revoke (delete the row), but every request needs a lookup.

**Signed tokens.** On login, the server creates a token that *contains* the user id and an expiry time, plus a **signature** that proves the server made it. The client sends it back, usually as `Authorization: Bearer <token>`. The server checks the signature and reads the user id, with no lookup. **JWTs** (JSON Web Tokens) are the best-known format. The trade-off: a token can't easily be cancelled before it expires, so expiry times are kept short.

Either way, the secret part (the session id or the token) must be **unguessable**, which means made by a cryptographically secure random generator:

```python
import secrets

print(secrets.token_urlsafe(32))
# e.g. 'k3T9...' (43 random URL-safe characters)
```

Never use the `random` module for anything security-related; its output can be predicted.

## 4. Signing with HMAC

How can a server tell that a token it receives is one it issued, and that nobody changed the user id inside? With an **HMAC** (Hash-based Message Authentication Code): a hash of the message **mixed with a secret key** only the server knows.

```python
import hashlib
import hmac

SECRET = b"server-only-secret"   # in real life: from an environment variable

def signature(message: bytes) -> str:
    return hmac.new(SECRET, message, hashlib.sha256).hexdigest()

msg = b'{"user_id": 7}'
sig = signature(msg)
print(sig == signature(b'{"user_id": 7}'))   # True: same message, same signature
print(sig == signature(b'{"user_id": 1}'))   # False: change one byte and it's different
```

Anyone can **read** the message, but without the secret they can't produce a valid signature for a modified one. If an attacker changes `7` to `1` to become user 1, the signature no longer matches and the server rejects the token.

A token is then just the message and its signature, packed into text that's safe in a header. **Base64** is an encoding that turns any bytes into letters, digits and a couple of symbols; the URL-safe variant uses `-` and `_`:

```python
import base64
import json

payload = {"user_id": 7, "exp": 1_800_000_000}
body = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
token = body + "." + signature(body.encode())
print(token[:20] + "...")
# eyJ1c2VyX2lkIjogNywg...
```

Base64 is **encoding, not encryption**: anyone can decode it and read the payload. Never put secrets inside a token. The signature only guarantees it hasn't been **changed**.

The `exp` (expiry) field is a Unix timestamp: seconds since 1 January 1970. When verifying, compare it with the current time and reject expired tokens. In the exercise, "now" is passed in as an argument so tests can pretend it's any time they like.

## 5. Constant-time comparison

When you check a signature, don't use `==`:

```python
if given_sig == expected_sig:              # leaks timing information
if hmac.compare_digest(given_sig, expected_sig):   # correct
```

`==` on strings stops at the first character that differs, so a wrong signature that starts with the right characters takes very slightly longer to reject. With enough measurements, an attacker can use that timing to work out a valid signature one character at a time. `hmac.compare_digest` always takes the same time, whatever the inputs. It's a one-word change; always make it when comparing secrets.

## 6. Authorisation: checking every time

Authentication tells you the request is from user 7. That alone doesn't mean user 7 may do what they're asking. The most common serious bug in real APIs is forgetting this check:

```python
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, user=Depends(current_user)):
    repo.delete(note_id)          # BUG: any logged-in user can delete ANY note
```

User 7 just changes the id in the URL to 8, 9, 10… and deletes everyone's notes. This is called **broken access control** (or IDOR, insecure direct object reference), and it's number one on the OWASP Top 10 list. The fix is a rule, checked on every request that touches someone's data:

```python
def can_edit(user: dict, note: dict) -> bool:
    return user["role"] == "admin" or note["owner_id"] == user["id"]
```

Then in the handler: load the note, 404 if it doesn't exist, 403 if `can_edit` is false, and only then change anything. Keep rules like this in one small, well-tested function rather than sprinkling `if` statements through handlers; you'll write and test one in the practice.

A safe default is **deny unless allowed**: start from "no", and list exactly who gets "yes".

## 7. The OWASP Top 10, at a junior level

**OWASP** (the Open Worldwide Application Security Project) publishes a list of the most common web security risks. You don't need to memorise it; you need to recognise the big ones in code you write and review:

| Risk | What it looks like | Your defence |
|---|---|---|
| Broken access control | user 7 can read or edit user 8's data | check ownership/role on every request |
| Injection | SQL built with f-strings | parameters, always (*SQL from Python, safely*) |
| Cryptographic failures | plain or SHA-256 passwords; HTTP instead of HTTPS | Argon2/bcrypt; HTTPS everywhere |
| Security misconfiguration | debug mode on in production, default passwords | review settings before deploying |
| Vulnerable components | old library versions with known holes | keep dependencies updated |
| Identification and authentication failures | no rate limit on login, tokens that never expire | limit attempts; short expiry |

Two more habits cover a lot of ground:

- **Validate input at the boundary.** Every value from outside (body, query, headers, files) is untrusted until checked. Pydantic models in FastAPI do much of this for you: types, lengths, ranges.
- **Keep secrets out of your repository.** Secret keys, database passwords and API keys come from environment variables. If one is ever committed, rotate it (make a new one, revoke the old) before anything else: deleting the commit doesn't undo the leak.

## Common mistakes

**Hashing passwords with SHA-256 or MD5.** Fast hashes are crackable. Use a password-hashing library.

**Comparing secrets with `==`.** Use `hmac.compare_digest`.

**Trusting the client.** A request body saying `{"role": "admin"}` or `{"owner_id": 1}` is just text someone typed. Take the user's identity from the verified token, never from the body.

**Returning 404 vs 403 inconsistently.** Some APIs return 404 instead of 403 for other people's resources, so attackers can't even learn that they exist. Either is defensible; pick one and be consistent.

**Error messages that help attackers.** "No account with that email" vs "wrong password" tells an attacker which emails are registered. Say "invalid email or password" for both.

**Rolling your own crypto.** HMAC for signing and a library for password hashing are fine. Inventing your own encryption scheme is not.

## Recap

- **Authentication** = who you are (401 if unknown); **authorisation** = what you may do (403 if not allowed).
- Store passwords with a **salted, slow** hash (Argon2, scrypt, bcrypt) from a library, never plain or with SHA-256.
- Sessions keep state on the server; **signed tokens** carry it, protected by an **HMAC** signature and a short **expiry**.
- Base64 is readable by anyone; the signature only proves the token wasn't changed.
- Compare secrets with `hmac.compare_digest`; generate them with `secrets`.
- Check authorisation on **every** request that touches someone's data: deny unless allowed.
- Validate input at the boundary, use parameters for SQL, keep secrets in the environment.
