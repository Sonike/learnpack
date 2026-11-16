# A (deliberately simple) email check

A **regular expression** (regex) describes a pattern of text. Python's `re` module checks text against a pattern. Write a simple check for "looks like an email address", so a sign-up form can catch obvious typos.

```python
def is_valid_email(s: str) -> bool: ...
```

- `s` is whatever the user typed.
- Return `True` if **the whole string** matches this shape, else `False`:
  - one or more characters that are not `@` and not whitespace (the part before `@`),
  - exactly one `@`,
  - one or more characters that are not `@` and not whitespace,
  - a dot, then **at least two letters** at the very end (like `.com` or `.uk`).

In regex terms: `[^@\s]+@[^@\s]+\.[A-Za-z]{2,}`. Use `re.fullmatch(pattern, s)`, which only succeeds if the **entire** string matches, and write the pattern as a raw string (`r"..."`) so the backslashes reach `re` unchanged. `fullmatch` returns a match object or `None`; turn that into `True`/`False`.

This check is intentionally loose. Real email rules are far more complicated, and the only true test is sending a confirmation email.

## Example

```python
is_valid_email("ada@example.com")             # True
is_valid_email("first.last+news@mail.co.uk")  # True
is_valid_email("ada.example.com")             # False  (no @)
is_valid_email("ada@example")                 # False  (no .something at the end)
is_valid_email("ada @example.com")            # False  (space)
```
