# Slugify a title

A **slug** is the readable part of a web address: the blog post "Café au Lait: 10 Tips!" lives at `/posts/cafe-au-lait-10-tips`. Write `slugify(title)` that turns any title into a slug.

```python
def slugify(title: str) -> str: ...
```

The rules, in order:

1. Turn accented letters into plain ones (`é` → `e`, `Ü` → `U`) and drop any other non-ASCII characters. The standard library does this for you:
   ```python
   import unicodedata
   plain = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
   ```
   `NFKD` splits `é` into `e` plus a separate accent mark; encoding to ASCII with `"ignore"` drops the accent mark.
2. Lowercase everything.
3. Replace every **run** of characters that aren't `a`–`z` or `0`–`9` with a single `-`. Spaces, punctuation and underscores all count as separators, and several in a row become one dash.
4. Remove dashes from the start and end.

A title with no letters or digits at all gives an empty string.

The hidden tests are a **table**: a list of `(title, expected)` pairs checked in a loop. Here it is:

| title | slug |
|---|---|
| `"Hello World"` | `"hello-world"` |
| `"Café au Lait: 10 Tips!"` | `"cafe-au-lait-10-tips"` |
| `"  Leading and trailing  "` | `"leading-and-trailing"` |
| `"a -- b __ c"` | `"a-b-c"` |
| `"snake_case_name"` | `"snake-case-name"` |
| `"Ünïcödé Rocks"` | `"unicode-rocks"` |
| `"!!!"` | `""` |
| `""` | `""` |

> **Tip:** `re.sub(r"[^a-z0-9]+", "-", text)` does step 3 in one line. The `+` means "one or more", which is what turns `" -- "` into a single dash.
