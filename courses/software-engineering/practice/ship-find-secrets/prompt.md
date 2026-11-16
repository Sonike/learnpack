# Find secrets before they're committed

Teams often run a small check before every commit (a **pre-commit hook**) that refuses to commit anything that looks like a secret. Write its core.

```python
def find_secrets(text: str) -> list[int]:
```

- `text`: the contents of a file about to be committed.
- Return the **line numbers** (starting at 1) of every line that looks like it contains a secret, in order. Each line appears at most once.

A line looks like a secret if **any** of these match somewhere in it:

1. **AWS access key:** `AKIA` followed by exactly 16 capital letters or digits (regex: `AKIA[0-9A-Z]{16}`).
2. **`sk-` style API key:** `sk-` followed by at least 20 letters, digits, `-` or `_` (regex: `sk-[A-Za-z0-9_-]{20,}`).
3. **Hard-coded secret in code:** a name containing `password`, `secret`, `api_key` or `token` (any case), optionally followed by a closing quote, then `=` or `:`, then a **non-empty quoted string**. For example `password = "hunter2"`, `"api_key": 'abc'`, `DB_TOKEN="x"`.
4. **`.env` style line:** the whole line (after stripping spaces) is `NAME=value`, where `NAME` is made of capital letters, digits and `_`, contains `PASSWORD`, `SECRET`, `TOKEN` or `API_KEY`, and `value` is non-empty with no spaces. For example `DB_PASSWORD=hunter2`.

These must **not** be flagged: `password = os.environ["DB_PASSWORD"]`, `SECRET_KEY=` (empty, as in a `.env.example`), `token = ""`, and ordinary code.

> **Note:** a real scanner such as `gitleaks` has hundreds of patterns. Four are enough to see how they work.

## Example

```python
text = '''import os
AWS_KEY = "AKIAABCDEFGHIJKLMNOP"
password = os.environ["DB_PASSWORD"]
api_key = "abc123"
SECRET_KEY=
STRIPE_SECRET=whsec_123'''

find_secrets(text)   # [2, 4, 6]
```
