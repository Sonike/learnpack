# Redact secrets before logging

Even careful teams sometimes log a whole request or config by accident. A **redaction** step is the safety net: it masks sensitive values before anything is written.

```python
MASK = "***"

def redact(data: dict) -> dict:
```

- `data`: a dictionary about to be logged. Values can be anything: strings, numbers, `None`, nested dicts, and lists (which may contain dicts).
- Return a **new** dictionary with the same structure, where the value of every **sensitive key** is replaced by `"***"`. **Don't change the original** `data`.

A key is **sensitive** if, after converting it to lower case and replacing `-` with `_`, it **contains** any of: `password`, `token`, `secret`, `authorization`, `api_key`. So `"Password"`, `"access_token"`, `"X-API-Key"` and `"client_secret"` are all sensitive.

Work **recursively**: redact inside nested dicts, and inside dicts that sit in lists, at any depth. A sensitive key's whole value is masked, even if it is itself a dict.

## Example

```python
redact({
    "user": "ada",
    "password": "hunter2",
    "headers": {"Authorization": "Bearer abc", "Accept": "json"},
    "items": [{"sku": 1, "api_key": "k"}],
})
# {'user': 'ada',
#  'password': '***',
#  'headers': {'Authorization': '***', 'Accept': 'json'},
#  'items': [{'sku': 1, 'api_key': '***'}]}
```
