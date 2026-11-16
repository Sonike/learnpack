# Classify a review comment

On a pull request, the author needs to know which comments **must** be fixed before merging and which are optional. Many teams use **conventional prefixes** for that: `nit:` for a small optional polish, `question:` when the reviewer just wants to understand, `praise:` for something done well.

Write `classify_comment(text: str) -> str` that returns one of `"blocking"`, `"nit"`, `"question"` or `"praise"`, using these rules **in order**:

1. **Prefix.** If the comment has a label before its first `:`, look it up (case-insensitive, spaces ignored):
   - `nit` or `nitpick` → `"nit"`
   - `question` → `"question"`
   - `praise` or `kudos` → `"praise"`
   - `blocking`, `issue` or `must` → `"blocking"`

   A label that isn't in this list doesn't count; carry on to rule 2.
2. **Question mark.** If the comment (stripped) ends with `?` → `"question"`.
3. **Praise words.** If any word in the comment is one of `nice`, `great`, `love`, `thanks`, `thank`, `clean`, `neat` (case-insensitive, whole words) → `"praise"`.
4. **Otherwise** → `"blocking"`. Google's review guide makes the same assumption: an unlabelled comment is treated as something the author should address.

## Examples

```python
classify_comment("nit: extra blank line here")              # 'nit'
classify_comment("Question: why a list and not a set?")     # 'question'
classify_comment("What happens if items is empty?")         # 'question'
classify_comment("Love how small this function is!")       # 'praise'
classify_comment("This query is open to SQL injection.")    # 'blocking'
classify_comment("Note: see the docs for retries")          # 'blocking'  (unknown label, no ?, no praise word)
```

> **Hint:** `text.split(":", 1)` gives you the part before the first colon. `re.findall(r"[a-z]+", text.lower())` gives you the words.
