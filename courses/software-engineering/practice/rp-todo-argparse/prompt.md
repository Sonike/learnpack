# A command-line interface with argparse

Command-line tools like `git` have **subcommands**: `git add`, `git commit`, `git log`. Python's `argparse` module builds that for you, including `--help` and error messages. Build the parser for a small to-do app.

```python
def build_parser() -> argparse.ArgumentParser:
```

Return a parser (with `prog="todo"`) that understands three subcommands. Store the chosen subcommand in `args.command`, and make choosing one required.

| Command | Arguments | Example | Resulting `args` |
|---|---|---|---|
| `add` | `text` (positional), `--priority` with choices `low`, `normal`, `high` (default `normal`) | `todo add "Buy milk" --priority high` | `command="add", text="Buy milk", priority="high"` |
| `list` | `--all` flag (`store_true`) | `todo list --all` | `command="list", all=True` |
| `done` | `id` (positional, converted to `int`) | `todo done 3` | `command="done", id=3` |

The tests call `build_parser().parse_args([...])` with a list of strings, which is exactly what your shell would pass after `todo`. Bad input (like `todo done abc`) makes argparse print an error and raise `SystemExit`; that's the behaviour we want.

## Example

```python
parser = build_parser()
args = parser.parse_args(["add", "Buy milk"])
args.command, args.text, args.priority   # ("add", "Buy milk", "normal")
parser.parse_args(["done", "3"]).id      # 3   (an int, not "3")
```

Hint: `subparsers = parser.add_subparsers(dest="command", required=True)`, then `add = subparsers.add_parser("add")`.
