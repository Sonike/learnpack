# Split a command line into its parts

Every terminal command has the same shape: a **command**, then **flags** (options that start with `-`, like `-l` or `--all`), then **arguments** (what the command works on, like a file name). Quotes keep a name with spaces together: `"My Documents"` is one argument.

```python
def parse_command(line: str) -> tuple[str, list[str], list[str]]: ...
```

- `line` is one command line as typed, e.g. `'ls -la "My Documents"'`.
- Return `(command, flags, arguments)`:
  - `command`: the first word;
  - `flags`: every later word that starts with `-`, in order;
  - `arguments`: every other later word, in order, with quotes removed.
- An empty or blank line returns `("", [], [])`.

Use `shlex.split(line)` from the standard library to split the line: it understands quotes the way a shell does.

## Example

```python
parse_command("ls -la projects")
# ("ls", ["-la"], ["projects"])
parse_command('cp -r "My Documents" backup --verbose')
# ("cp", ["-r", "--verbose"], ["My Documents", "backup"])
parse_command("   ")
# ("", [], [])
```
