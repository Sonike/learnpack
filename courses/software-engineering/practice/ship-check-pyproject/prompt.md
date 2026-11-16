# Check a `pyproject.toml`

Write a small checker a team could run in CI to catch common mistakes in a project's `pyproject.toml`.

```python
def check_pyproject(text: str) -> list[str]:
```

- `text`: the contents of a `pyproject.toml` file.
- Return a list of problem messages, in the order below. An empty list means the file is fine.

Use the standard `tomllib` module: `tomllib.loads(text)` turns TOML text into nested dicts and lists, and raises `tomllib.TOMLDecodeError` if the text isn't valid TOML.

## Checks, in order

1. If the text isn't valid TOML, return `["invalid TOML"]` and stop.
2. If there's no `[project]` table, return `["missing [project] table"]` and stop.
3. If `[project]` has no `requires-python`, add `"missing requires-python"`.
4. For each entry in `project.dependencies` (if any), in order: if it contains none of the characters `<`, `>`, `=`, `!`, `~`, it has no version constraint, so add `"unpinned dependency: <entry>"` (the entry stripped of spaces).
5. Look for a dependency named `pytest` in **any** list under `[dependency-groups]` or `[project.optional-dependencies]`. A requirement's name is the part before the first `<`, `>`, `=`, `!`, `~`, `;`, `[` or space, compared in lower case. If none is found, add `"missing test dependency (pytest)"`.

## Example

```python
text = '''
[project]
name = "habit-api"
dependencies = ["fastapi>=0.115", "requests"]

[dependency-groups]
dev = ["ruff>=0.6"]
'''
check_pyproject(text)
# ['missing requires-python',
#  'unpinned dependency: requests',
#  'missing test dependency (pytest)']
```
