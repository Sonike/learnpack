# Resolve a path by hand

When you type `cd ../data` or open `./notes/todo.txt`, the computer works out the full, **absolute** path from your current folder. Write that logic yourself for macOS/Linux-style paths (folders separated by `/`).

```python
def resolve(cwd: str, path: str) -> str: ...
```

- `cwd` is the current working directory, always an absolute path such as `"/home/ada/projects"`.
- `path` is what the user typed. It may be absolute (starts with `/`) or relative (doesn't).
- Return the clean absolute path:
  - an absolute `path` ignores `cwd`;
  - `.` means "this folder" and is dropped;
  - `..` means "the parent folder"; `..` at the root `/` stays at `/`;
  - empty parts from repeated slashes (`a//b`) or a trailing slash are ignored;
  - the result starts with `/` and never ends with `/` (except the root itself, `"/"`).

Don't use `os.path` or `pathlib` in your answer; the tests compare yours with `posixpath.normpath`.

**Hint:** start from a list of folder names (from `cwd`, or empty if `path` is absolute), then walk through `path.split("/")` and append or pop.

## Example

```python
resolve("/home/ada", "projects/app")     # "/home/ada/projects/app"
resolve("/home/ada/projects", "../data") # "/home/ada/data"
resolve("/home/ada", "/etc//hosts/")     # "/etc/hosts"
resolve("/", "../..")                    # "/"
```
