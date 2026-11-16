import argparse


def build_parser() -> argparse.ArgumentParser:
    """Parser for: todo add TEXT [--priority P] | todo list [--all] | todo done ID."""
    parser = argparse.ArgumentParser(prog="todo", description="A tiny to-do list.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="add a task")
    add.add_argument("text", help="what to do")
    add.add_argument("--priority", choices=["low", "normal", "high"], default="normal")

    list_cmd = subparsers.add_parser("list", help="show tasks")
    list_cmd.add_argument("--all", action="store_true", help="include finished tasks")

    done = subparsers.add_parser("done", help="mark a task as finished")
    done.add_argument("id", type=int, help="the task's number")

    return parser
