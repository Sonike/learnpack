# HTTP in depth

## Why this matters

HTTP is the language of the web, and of nearly every API you'll build or call. Frameworks hide it behind decorators and helper functions, but the moment something goes wrong (a 415 you don't understand, a body that arrives empty, a cookie that won't stick) you need to read the raw request and response and see the problem. The good news: HTTP is plain text with a simple shape, and you can learn all of it that matters in one sitting.

## 1. A request is just text

When your browser loads `https://api.example.com/tasks?status=todo`, it sends text like this (over the TLS connection from *How the internet works*):

```
GET /tasks?status=todo HTTP/1.1
Host: api.example.com
Accept: application/json
User-Agent: Mozilla/5.0

```

Every HTTP request has the same three parts:

```
GET /tasks?status=todo HTTP/1.1      <- 1. request line: METHOD  TARGET  VERSION
Host: api.example.com                <- 2. headers: one "Name: value" per line
Accept: application/json
                                     <- a blank line ends the headers
(optional body)                      <- 3. body: the data being sent, if any
```

- The **request line** says what to do (`GET`), to what (`/tasks?status=todo`, the path plus query), and which HTTP version.
- **Headers** are extra information, as `Name: value` pairs. Header names are **case-insensitive**: `Content-Type`, `content-type` and `CONTENT-TYPE` are the same header.
- A **blank line** separates headers from the body.
- The **body** carries data, for example the new task you're creating. `GET` requests usually have none.

Lines end with `\r\n` (carriage return + line feed), a leftover from typewriters that HTTP/1.1 still uses. So the blank line is really `\r\n\r\n`.

Here's a request that sends data:

```
POST /tasks HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 27

{"title": "Write the docs"}
```

`Content-Type` says what format the body is in. `Content-Length` says how many **bytes** it is, so the server knows where it ends.

## 2. A response is just text too

The server answers in the same shape:

```
HTTP/1.1 201 Created
Content-Type: application/json
Content-Length: 51

{"id": 7, "title": "Write the docs", "done": false}
```

The first line is the **status line**: version, a **status code** (a number), and a **reason phrase** (a short human description). Then headers, a blank line, and the body.

You can see real requests and responses yourself with `curl -v` (the `-v` means verbose). Lines starting with `>` are what curl sent; `<` is what came back:

```bash
curl -v https://example.com/
```

```
> GET / HTTP/2
> Host: example.com
> User-Agent: curl/8.7.1
> Accept: */*
>
< HTTP/2 200
< content-type: text/html
< content-length: 1256
<
<!doctype html>
...
```

(Modern sites often use HTTP/2, which sends the same information in a compact binary form. The methods, headers and status codes are identical, so everything here still applies.)

> **Try it:** your browser's developer tools (F12 or right-click → Inspect, then the **Network** tab) show every request a page makes. Reload any site and click a request to see its headers.

## 3. Methods: what you want to do

The **method** (sometimes called the verb) says what action the client wants. Five cover almost everything:

| Method | Meaning | Example |
|---|---|---|
| `GET` | read a resource | `GET /tasks/7` |
| `POST` | create something new (or trigger an action) | `POST /tasks` with a body |
| `PUT` | replace a resource completely | `PUT /tasks/7` with the full task |
| `PATCH` | change part of a resource | `PATCH /tasks/7` with `{"done": true}` |
| `DELETE` | remove a resource | `DELETE /tasks/7` |

Two properties matter when things go wrong on the network:

- **Safe** methods don't change anything on the server. `GET` (and `HEAD`, `OPTIONS`) are safe. Browsers, caches and search engines call `GET` freely, so a `GET` must never delete or charge anything.
- **Idempotent** methods have the same effect whether you send them once or ten times. `GET`, `PUT` and `DELETE` are idempotent: deleting task 7 twice leaves it just as deleted. `POST` is **not**: posting an order twice creates two orders. `PATCH` usually isn't guaranteed to be either.

Why care? Networks fail. If a request times out, you don't know whether the server got it. Retrying an idempotent request is safe; retrying a `POST` might charge a customer twice. You'll build retries in *Consuming APIs*.

## 4. Status codes: what happened

The status code is a three-digit number. The first digit is the **family**:

| Family | Meaning |
|---|---|
| `1xx` | informational (rare in practice) |
| `2xx` | success |
| `3xx` | redirection: look somewhere else |
| `4xx` | **client** error: the request was wrong |
| `5xx` | **server** error: the request was fine, the server failed |

The 4xx/5xx split is the most useful thing to remember: 4xx means "fix your request", 5xx means "our bug, not yours".

The ten you'll use constantly:

| Code | Name | Use it when |
|---|---|---|
| 200 | OK | success, with a body (most `GET`s) |
| 201 | Created | a `POST` created something; return the new thing |
| 204 | No Content | success with no body (often `DELETE`) |
| 301 | Moved Permanently | the resource has a new URL (in the `Location` header) |
| 400 | Bad Request | malformed request: invalid JSON, a missing field |
| 401 | Unauthorized | you're **not logged in** (no or bad credentials) |
| 403 | Forbidden | you're logged in but **not allowed** to do this |
| 404 | Not Found | no such resource |
| 409 | Conflict | clashes with current state: duplicate email, editing a stale version |
| 500 | Internal Server Error | the server crashed or hit a bug |

401 vs 403 confuses everyone, partly because 401's official name says "Unauthorized" when it really means "unauthenticated". Use **401 = who are you?** and **403 = I know who you are, and no**. You'll come back to this in *Auth and security basics*.

## 5. Content-Type and JSON

The body is just bytes. The `Content-Type` header says how to read them:

| Content-Type | Body is |
|---|---|
| `application/json` | JSON, the default for APIs |
| `text/html; charset=utf-8` | a web page |
| `text/plain` | plain text |
| `application/x-www-form-urlencoded` | an HTML form: `name=Ada&age=30` |

Almost every API you build will send and receive JSON. In Python:

```python
import json

body = json.dumps({"title": "Write the docs", "done": False})
print(body)                 # {"title": "Write the docs", "done": false}
print(json.loads(body))     # {'title': 'Write the docs', 'done': False}
```

### Bytes, not characters

`Content-Length` counts **bytes**, and text is sent as UTF-8, where one character can take more than one byte:

```python
text = '{"name": "Adébáyọ̀"}'
print(len(text))                    # 20  characters
print(len(text.encode("utf-8")))    # 25  bytes
```

If you send `Content-Length: 20` for that body, the client stops reading 5 bytes early and the JSON is cut off. Always measure the **encoded** body. (By default `json.dumps` escapes non-ASCII characters as `é` and so on, which hides this problem; with `ensure_ascii=False` you get the real characters and the byte count matters.)

## 6. HTTP is stateless

Each request stands alone. The server doesn't remember that the same browser sent a request a second ago. That makes servers simpler and easier to scale: any of ten identical servers can answer any request.

But then how does a site know you're logged in? The client sends something that identifies it **with every request**:

- **Cookies.** The server's response includes `Set-Cookie: session=abc123; HttpOnly; Secure`. The browser stores it and automatically sends `Cookie: session=abc123` on every later request to that site. The server looks up `abc123` in its **session** store to find out who you are.
- **Tokens.** API clients usually send a header like `Authorization: Bearer eyJhbGciOi...` on each request.

`HttpOnly` stops JavaScript in the page from reading the cookie, and `Secure` means it's only sent over HTTPS. *Auth and security basics* goes deeper.

## 7. Building HTTP by hand in Python

There's no magic in any of this. Here's a response built with string formatting:

```python
import json
from http import HTTPStatus

def build(status: int, data: dict) -> str:
    body = json.dumps(data)
    reason = HTTPStatus(status).phrase       # 404 -> "Not Found"
    return (
        f"HTTP/1.1 {status} {reason}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        f"\r\n"
        f"{body}"
    )

print(build(404, {"error": "no such task"}))
# HTTP/1.1 404 Not Found
# Content-Type: application/json
# Content-Length: 25
#
# {"error": "no such task"}
```

And reading a request is a matter of splitting on the right separators: `\r\n\r\n` between headers and body, `\r\n` between lines, `": "` inside a header, `" "` in the request line, `?` between path and query. You'll write both directions in the practice exercises, and then a framework will do it for you in *Building an API with FastAPI*.

## Common mistakes

**Changing data with `GET`.** A link like `/tasks/7/delete` fetched with `GET` will be "clicked" by link previews, crawlers and browser prefetching. Use `DELETE` (or `POST`).

**Returning 200 for errors.** `200 OK` with `{"error": "not found"}` breaks every client that checks the status. Use the right code; put details in the body.

**Returning 500 for bad input.** If the client sent invalid data, that's a 400 (or 422), not a crash. A 500 should mean a bug on your side.

**Counting characters for `Content-Length`.** Encode first, then count bytes.

**Forgetting `Content-Type: application/json` when sending JSON.** Many servers, including FastAPI, will then not parse your body. With `curl`, add `-H "Content-Type: application/json"`.

**Comparing header names exactly.** `headers["Content-Type"]` misses a client that sent `content-type`. Lower-case names when you store them.

## Recap

- A request is a **request line** (method, target, version), **headers**, a blank line, and an optional **body**. A response swaps the first line for a **status line**.
- Methods: `GET` reads, `POST` creates, `PUT` replaces, `PATCH` updates part, `DELETE` removes. `GET` is **safe**; `GET`, `PUT`, `DELETE` are **idempotent**; `POST` isn't.
- Status families: 2xx success, 3xx redirect, 4xx client's fault, 5xx server's fault. Know 200, 201, 204, 301, 400, 401, 403, 404, 409, 500.
- `Content-Type` says how to read the body; `Content-Length` is in **bytes**.
- HTTP is **stateless**; cookies and tokens identify the client on every request.
