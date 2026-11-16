# Your first solution: a greeting

This exercise is about the loop you'll use for every exercise in this course: **read the task → write code → Run → Check → fix → Check again**.

```python
def greet(name: str) -> str: ...
```

- `name` is whatever someone typed, possibly with extra spaces or odd capitals.
- Remove spaces at the start and end (`.strip()`), then capitalise each word (`.title()`).
- Return `"Hello, <name>!"`.
- If nothing is left after stripping (an empty or blank name), return `"Hello, stranger!"`.

**Return** the text; don't `print` it. The tests call `greet(...)` and look at what comes back.

## Example

```python
greet("ada")                 # "Hello, Ada!"
greet("  grace HOPPER ")     # "Hello, Grace Hopper!"
greet("   ")                 # "Hello, stranger!"
```
