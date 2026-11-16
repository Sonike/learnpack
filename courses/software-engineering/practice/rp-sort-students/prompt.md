# Sort students by grade, then name

A teacher wants the class list sorted best grade first, and alphabetically by name when two students have the same grade.

```python
def sort_students(records: list[dict]) -> list[dict]:
```

- `records` is a list of dicts like `{"name": "Ada", "grade": 91}`. Some records have extra keys (like `"id"`); keep them as they are.
- Return a **new** sorted list: highest `grade` first; equal grades sorted by `name` A→Z.
- Don't change the list you were given (use `sorted`, not `.sort()`).
- Records with the same grade **and** the same name keep their original order. Python's sort is *stable*, so you get this for free.

## Example

```python
sort_students([
    {"name": "Grace", "grade": 85},
    {"name": "Ada", "grade": 91},
    {"name": "Alan", "grade": 85},
])
# [{"name": "Ada", "grade": 91}, {"name": "Alan", "grade": 85}, {"name": "Grace", "grade": 85}]
```

Hint: a `key` function can return a tuple. Tuples compare item by item, and `-grade` sorts numbers from high to low.
