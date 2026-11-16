# Find the first bad version (how git bisect works)

Your app worked in an old release and is broken now. Somewhere in between, one change broke it, and every version after that is broken too. Testing each version one by one is slow, so you'll **halve the search each time**: check the middle version, then throw away the half that can't contain the answer. This is exactly what `git bisect` does with commits.

```python
def first_bad_version(versions: list[str], is_bad) -> int:
```

- `versions` is a list of version names in order, oldest first, e.g. `["v1", "v2", ..., "v100"]`.
- `is_bad(version)` is a function you call with a version name. It returns `True` if that version is broken. Calling it is expensive (imagine it builds the app and runs the tests), so call it as few times as possible.
- Return the **index** of the first bad version, or `-1` if none are bad.
- You can rely on this: once a version is bad, every later version is bad too.

The tests count your calls: for 1,000 versions you may call `is_bad` at most 11 times. Checking every version would take up to 1,000.

## Example

```python
versions = ["v1", "v2", "v3", "v4", "v5", "v6"]
first_bad_version(versions, lambda v: v in {"v4", "v5", "v6"})   # 3
first_bad_version(versions, lambda v: False)                      # -1
```

Hint: keep two numbers, `low` and `high`, that bound where the answer can be. Look at `versions[(low + high) // 2]` and move one of them.
