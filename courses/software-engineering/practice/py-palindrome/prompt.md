# Is it a palindrome?

A palindrome reads the same forwards and backwards once you ignore spaces, punctuation and capitals: *"A man, a plan, a canal: Panama"*.

```python
def is_palindrome(s: str) -> bool: ...
```

- `s` is any text.
- Keep only the letters (`ch.isalpha()`), lowercase them, and check whether the result equals its reverse (`text[::-1]`).
- Text with no letters at all (including `""`) counts as a palindrome: there's nothing that differs.

## Example

```python
is_palindrome("racecar")                          # True
is_palindrome("A man, a plan, a canal: Panama")   # True
is_palindrome("hello")                            # False
is_palindrome("")                                 # True
```
