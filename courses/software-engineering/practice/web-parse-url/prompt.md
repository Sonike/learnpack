# Take a URL apart by hand

Write `parse_url(url)` that splits a URL into its parts using only string methods (`split`, `partition`, `lower`, ...). The tests compare your answers with Python's own `urllib.parse`, so this is a chance to see there's no magic in it.

```python
def parse_url(url: str) -> dict: ...
```

`url` is an absolute URL like `https://shop.example.com:8443/products/42?colour=red&size=m#reviews`. Return a dict with exactly these keys:

| Key | Value | Rules |
|---|---|---|
| `"scheme"` | `"https"` | the part before `://`, lower-cased |
| `"host"` | `"shop.example.com"` | lower-cased, without the port |
| `"port"` | `8443` | an `int`. If the URL has no port, use the default: `80` for `http`, `443` for `https` |
| `"path"` | `"/products/42"` | `"/"` if the URL has no path |
| `"query"` | `{"colour": "red", "size": "m"}` | a dict from the part after `?`; `{}` if there's no query. A key with no `=` gets `""` |

The **fragment** (after `#`) is never sent to the server: drop it before anything else.

Suggested order: drop the fragment, split off the scheme at `://`, split the query off at `?`, split the path off at the first `/`, then split host and port at `:`.

## Example

```python
parse_url("HTTPS://Shop.Example.com/products/42?colour=red&size=m#reviews")
# {'scheme': 'https', 'host': 'shop.example.com', 'port': 443,
#  'path': '/products/42', 'query': {'colour': 'red', 'size': 'm'}}
parse_url("http://localhost:8000")
# {'scheme': 'http', 'host': 'localhost', 'port': 8000, 'path': '/', 'query': {}}
```
