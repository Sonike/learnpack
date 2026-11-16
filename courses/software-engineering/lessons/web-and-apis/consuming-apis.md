# Consuming APIs

## Why this matters

Very little software stands alone. A shop calls a payment API, a delivery app calls a maps API, your backend calls another team's service. Calling an API once in a demo is easy. Calling it reliably in production is a different job: results come in pages, the service limits how fast you can ask, the network drops requests, and the API key must never end up on GitHub. This lesson covers the habits that separate a script that works on Tuesday from a client that keeps working.

## 1. What an API is

An **API** (Application Programming Interface) is a set of operations one program offers to others. A **web API** offers them over HTTP: you send a request to a URL, it sends back data, usually JSON.

Most web APIs follow **REST** conventions (REpresentational State Transfer). You don't need the theory; you need the habits:

- URLs name **resources** (things), using **nouns**, usually plural: `/users`, `/orders`.
- The HTTP **method** says what to do with them (from *HTTP in depth*).
- One item is addressed by its id: `/users/42`.
- Things that belong to something else are **nested**: `/users/42/orders` is "the orders of user 42".

```
GET    /users            list users
POST   /users            create a user
GET    /users/42         get user 42
PATCH  /users/42         update part of user 42
DELETE /users/42         delete user 42
GET    /users/42/orders  list user 42's orders
```

Compare this with verb-style URLs like `/getUser?id=42` or `/deleteOrder`. They work, but you have to learn every URL separately. With REST conventions, once you know the resource names, you can guess the rest.

## 2. Reading API docs

Before writing code, read the docs and find five things:

1. **The base URL**, e.g. `https://api.example.com/v1`.
2. **Authentication**: how to send your key (usually a header).
3. **The endpoint** you need: method, path, parameters, and an example response.
4. **Errors**: what status codes and error bodies look like.
5. **Limits**: page sizes and rate limits.

Then make one request by hand, with `curl` or your browser, and look at the real response before writing any code. Real responses often differ from the docs in small ways.

```bash
curl -s "https://api.github.com/repos/python/cpython" | head -5
```

```
{
  "id": 81598961,
  "node_id": "MDEwOlJlcG9zaXRvcnk4MTU5ODk2MQ==",
  "name": "cpython",
  "full_name": "python/cpython",
```

## 3. Making requests from Python

The standard library can do it with `urllib.request`:

```python
import json
import urllib.request

with urllib.request.urlopen("https://api.github.com/repos/python/cpython", timeout=10) as resp:
    print(resp.status)                       # 200
    data = json.loads(resp.read().decode("utf-8"))
print(data["full_name"], data["stargazers_count"])
# python/cpython 69000   (the number will have changed)
```

In real projects most people use **`requests`** or **`httpx`**, third-party libraries with a friendlier interface:

```python
import httpx   # pip install httpx

resp = httpx.get("https://api.github.com/repos/python/cpython", timeout=10)
resp.raise_for_status()      # raises an exception for any 4xx/5xx
print(resp.json()["full_name"])
# python/cpython
```

Two habits from day one:

- **Always set a timeout.** Without one, a server that never answers makes your program wait forever. Ten seconds is a reasonable default.
- **Check the status before using the body.** A 404 or 500 response often still has a JSON body, and it isn't the data you wanted.

> **Note:** the practice exercises in this lesson don't touch the network (the browser version can't open connections, and tests must be repeatable). Instead, the function that makes the request is **passed in** as an argument. This is called **dependency injection**, and it's how professionals test API clients too: in tests you pass a fake that returns canned responses.

## 4. Pagination

An API with a million orders won't return them all in one response. It returns a **page** at a time, and you ask for the next one. Two common styles:

**Page numbers (offset pagination):**

```
GET /orders?page=1&limit=100   -> orders 1-100
GET /orders?page=2&limit=100   -> orders 101-200
```

Simple, but if new orders arrive while you're reading, items shift between pages and you can see one twice or miss one.

**Cursors:** each response includes an opaque token pointing at where the next page starts:

```json
{"items": [{"id": 1}, {"id": 2}], "next_cursor": "b3JkZXI6Mg=="}
```

You send it back to get the next page, and stop when `next_cursor` is `null` (`None` in Python). Cursors stay correct while data changes, which is why large APIs (Stripe, Slack, GitHub's newer APIs) use them.

The loop for cursors, with the request function injected:

```python
def fetch_all(get_page):
    items, cursor = [], None
    while True:
        page = get_page(cursor)          # first call: cursor is None
        items.extend(page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            return items

# A fake API with three pages, for trying it out:
PAGES = {
    None: {"items": [1, 2], "next_cursor": "p2"},
    "p2": {"items": [3, 4], "next_cursor": "p3"},
    "p3": {"items": [5], "next_cursor": None},
}
print(fetch_all(lambda cursor: PAGES[cursor]))
# [1, 2, 3, 4, 5]
```

What if a buggy API keeps returning the same cursor? This loop never ends. A real client needs a safety limit on the number of pages, which you'll add in the exercise.

## 5. Rate limits

APIs limit how many requests you can make, say 60 per minute, so one client can't overwhelm them. Go over and you get **`429 Too Many Requests`**, often with a `Retry-After` header saying how many seconds to wait.

Respecting rate limits is part of being a good client: slow down, don't hammer.

## 6. Retries with exponential backoff

Some failures are temporary: `429 Too Many Requests`, `503 Service Unavailable` (the server is overloaded or restarting), or a timeout. Retrying after a pause often works. Others are permanent: `400`, `401`, `404`. Retrying those just gets the same answer, faster.

| Status | Retry? | What to do |
|---|---|---|
| 400, 404, 422 | no | your request is wrong; fix it |
| 401, 403 | no | check your key or permissions |
| 429 | yes, after waiting | slow down; honour `Retry-After` if given |
| 500 | maybe, once or twice | could be a passing glitch, could be a real bug |
| 502, 503, 504 | yes, with backoff | the server or something in front of it is temporarily unhappy |

If you retry immediately, and so do a thousand other clients, you keep the struggling server overloaded. **Exponential backoff** waits longer after each failure: 1 s, then 2 s, then 4 s, then 8 s. Each wait doubles:

```
delay = base_delay * 2 ** attempt     # attempt = 0, 1, 2, ...
        1s, 2s, 4s, 8s ...
```

Production code also adds a little randomness (**jitter**) to each delay so that clients don't all retry at the same instant, and gives up after a few tries.

A sketch, with `sleep` injected so tests don't actually wait:

```python
import time

def get_with_retry(call, retries=3, sleep=time.sleep):
    for attempt in range(retries + 1):
        status, body = call()
        if status not in (429, 503) or attempt == retries:
            return status, body
        sleep(2 ** attempt)    # 1, 2, 4 ...

attempts = iter([(503, None), (503, None), (200, {"ok": True})])
waits = []
print(get_with_retry(lambda: next(attempts), sleep=waits.append))
print(waits)
# (200, {'ok': True})
# [1, 2]
```

Passing `sleep=waits.append` records the delays instead of waiting, so the test is instant and you can check the backoff exactly. You'll write a fuller version in the practice.

Remember idempotency from *HTTP in depth*: retrying a `GET` is harmless; retrying a `POST` that created an order might create two. Many payment APIs accept an **idempotency key** header so a retried `POST` is recognised as a repeat.

## 7. API keys: never in your code

Most APIs identify you with a secret **API key**, sent in a header:

```
Authorization: Bearer sk_live_51H8...
```

That key is like a password with your credit card attached. Rules:

- **Never** write it in your source code. Code gets pushed to GitHub, and bots scan GitHub for keys within minutes.
- Keep it in an **environment variable** (a named value that the operating system hands to your program when it starts; the configuration lessons later in the course go deeper), and read it at run time:

```python
import os

api_key = os.environ.get("WEATHER_API_KEY")
if not api_key:
    raise SystemExit("Set WEATHER_API_KEY first, e.g. export WEATHER_API_KEY=...")

headers = {"Authorization": f"Bearer {api_key}"}
```

```bash
export WEATHER_API_KEY=abc123        # macOS/Linux; on Windows PowerShell: $env:WEATHER_API_KEY="abc123"
python weather.py
```

For development, many projects keep these in a `.env` file that's listed in `.gitignore` so it's never committed. The Twelve-Factor App guidelines in this lesson's resources call this "store config in the environment".

If a key does leak: **revoke it** in the provider's dashboard immediately, then create a new one. Deleting the commit isn't enough; it's already been copied.

## Common mistakes

**No timeout.** The program hangs forever on a slow server. Always pass `timeout=`.

**Using the body without checking the status.** `resp.json()["temperature"]` raises `KeyError: 'temperature'` because the body was `{"error": "invalid key"}`. Check the status (or call `raise_for_status()`) first, and read the error body: it usually says exactly what's wrong.

**Retrying everything.** Retrying a 401 three times just gets three 401s. Retry only temporary failures.

**Retrying with no limit.** An infinite retry loop turns an outage into a self-inflicted attack. Cap the attempts.

**Assuming one page is everything.** Your code works in testing with 20 items, then silently drops data in production when there are 2,000. Look for `next_cursor`, `next`, or a `Link` header.

**Committing the key.** Even in a private repo. Use environment variables from the start.

## Recap

- REST: resources as plural nouns in the URL, methods for actions, ids for single items, nesting for ownership.
- Read the docs for base URL, auth, endpoint, errors and limits; try one request by hand first.
- Always set a **timeout** and check the **status** before trusting the body.
- **Pagination**: keep requesting until there's no next cursor, with a page limit as a safety net.
- **429** means slow down; retry 429/503 with **exponential backoff** (1, 2, 4… seconds) and a cap; don't retry 4xx errors.
- API keys live in **environment variables**, never in code. A leaked key gets revoked.
