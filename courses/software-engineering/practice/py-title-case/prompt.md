# Title case, done properly

Python's `str.title()` capitalises every word: `"the lord of the rings".title()` gives `"The Lord Of The Rings"`. Book and film titles usually keep small words like *of* and *the* lowercase. Write a better version.

```python
def title_case(s: str, minor_words: set[str]) -> str: ...
```

- `s` is the title, in any mix of cases, words separated by spaces.
- `minor_words` is a set of lowercase words to keep lowercase, e.g. `{"a", "of", "the"}`.
- Rules:
  - every word is first made lowercase;
  - a word in `minor_words` stays lowercase, **except** the first word of the title, which is always capitalised;
  - every other word is capitalised (first letter upper, the rest lower; `word.capitalize()` does this).
- Join the words with single spaces (so extra spaces in `s` disappear). An empty string returns `""`.

## Example

```python
title_case("the lord of the rings", {"of", "the"})   # "The Lord of the Rings"
title_case("a TALE of two CITIES", {"a", "of"})      # "A Tale of Two Cities"
```
