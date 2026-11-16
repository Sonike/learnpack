# A mini shell

Build a tiny pretend terminal that keeps its folders in memory. It's the best way to make `pwd`, `cd`, `mkdir` and `ls` feel obvious.

```python
def run(commands: list[str]) -> list[str]: ...
```

- `commands` is a list of command lines, run in order, e.g. `["mkdir notes", "cd notes", "pwd"]`.
- The shell starts in the root folder `/`, which is empty.
- Return every line of output the commands printed, in order.

Store the folders as a **dict of dicts**: each folder is a dict that maps a child's name to that child's own dict. The root is `{}`; after `mkdir notes` it's `{"notes": {}}`.

| Command | What it does | Output |
|---|---|---|
| `pwd` | print the current folder's absolute path | `/` at the root, otherwise e.g. `/notes/2026` |
| `mkdir NAME` | create folder `NAME` inside the current folder | nothing; if it already exists: `mkdir: NAME: File exists` |
| `cd NAME` | move into child folder `NAME` | nothing; if it doesn't exist: `cd: no such file or directory: NAME` (and stay put) |
| `cd ..` | move up to the parent (at `/`, stay at `/`) | nothing |
| `cd /` | go back to the root | nothing |
| `ls` | list the current folder's children | one line per child, sorted A→Z; nothing if empty |
| anything else | | `command not found: WORD` (the first word) |

`NAME` is always a single folder name (no `/` inside). Ignore blank lines.

## Example

```python
run(["mkdir notes", "mkdir code", "ls", "cd notes", "pwd", "cd music", "cd ..", "pwd"])
# ["code", "notes", "/notes", "cd: no such file or directory: music", "/"]
```
