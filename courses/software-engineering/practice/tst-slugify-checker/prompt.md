# Catch eight broken slugifiers

You wrote `slugify` against a table of cases someone gave you. Now flip it round: write the tests. `check_slugify(fn)` asserts that `fn` follows the slug rules, and must catch **eight** different buggy versions.

```python
def check_slugify(fn) -> None: ...
```

- `fn` takes a title (`str`) and returns its slug (`str`).
- Return quietly when `fn` is correct; raise `AssertionError` (a failing `assert`) when it's wrong.

The rules, as before:

1. Accented letters become plain ASCII (`é` → `e`); other non-ASCII characters are dropped.
2. Everything is lowercase.
3. Every **run** of characters that aren't `a`–`z` or `0`–`9` (spaces, punctuation, underscores) becomes **one** `-`.
4. No dashes at the start or end.

The hidden tests run your checker on one correct `slugify` (must pass) and eight mutants (each must fail). Every mutant breaks exactly one thing: it keeps capitals, ignores accents, turns each separator into its own dash, forgets to strip dashes, strips only one end, replaces only spaces, drops digits, or keeps underscores.

To catch all eight you need **one test case per rule and per edge**: the ordinary case, accents, repeated separators, separators at both ends, punctuation that isn't a space, digits, and underscores. That's the skill this exercise trains: listing edge cases on purpose instead of hoping you thought of them.

> **Tip:** put your cases in a list of `(title, expected)` pairs and loop over them. That's a **table-driven test**, the same idea as `pytest.mark.parametrize`. Include the title in the assert message so you can see which case failed.
