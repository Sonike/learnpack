import argparse


def build_parser() -> argparse.ArgumentParser:
    """Parser for: todo add TEXT [--priority P] | todo list [--all] | todo done ID."""
    parser = argparse.ArgumentParser(prog="todo", description="A tiny to-do list.")
    # TODO: subparsers = parser.add_subparsers(dest="command", required=True)
    # TODO: "add": positional text, --priority with choices and default "normal"
    # TODO: "list": --all with action="store_true"
    # TODO: "done": positional id with type=int
    return parser


if __name__ == "__main__":
    parser = build_parser()
    for argv in (["add", "Buy milk", "--priority", "high"], ["list", "--all"], ["done", "3"]):
        try:
            print(argv, "->", parser.parse_args(argv))
        except SystemExit:
            print(argv, "-> argparse rejected this (see the error above)")
