# Resolve merge conflicts in code

When two branches change the same lines, Git can't choose for you. It writes **both** versions into the file between conflict markers and asks you to decide:

```
<<<<<<< HEAD
greeting = "Hello"
=======
greeting = "Hi there"
>>>>>>> feature/friendlier-greeting
```

- Between `<<<<<<<` and `=======` is **ours**: the branch you're on (`HEAD`).
- Between `=======` and `>>>>>>>` is **theirs**: the branch you're merging in.
- Everything outside the markers merged cleanly and stays as it is.

Write a function that resolves every conflict in a file the same way.

```python
def resolve_conflict(text: str, choose: str) -> str:
```

- `text` is the whole file's contents with conflict markers in it.
- `choose` is `"ours"`, `"theirs"` or `"both"` (ours first, then theirs). Anything else raises `ValueError`.
- Return the file with every conflict block replaced by the chosen lines and the marker lines removed. Keep every other line exactly as it was, including its line ending.
- A marker line is a line that **starts with** `<<<<<<<` or `>>>>>>>` (a branch name may follow), or is exactly `=======`.
- Raise `ValueError` for broken markers: a `=======` or `>>>>>>>` outside a conflict, a `<<<<<<<` inside one, a block with no `=======`, a block with two of them, or a file that ends inside a block.

## Example

```python
text = '''def greet(name):
<<<<<<< HEAD
    greeting = "Hello"
=======
    greeting = "Hi there"
>>>>>>> feature
    return f"{greeting}, {name}!"
'''
resolve_conflict(text, "theirs")
# 'def greet(name):\n    greeting = "Hi there"\n    return f"{greeting}, {name}!"\n'
```

Hint: `text.splitlines(keepends=True)` keeps the `\n` on each line, so `"".join(lines)` rebuilds the file. Track where you are with a variable such as `state = "outside" | "ours" | "theirs"`.
