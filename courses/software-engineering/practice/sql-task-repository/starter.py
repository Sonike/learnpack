import sqlite3
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    status: str  # "todo" or "done"


class TaskRepository:
    """All the SQL for tasks lives here. Callers only ever see Task objects."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        # TODO: CREATE TABLE IF NOT EXISTS tasks (...)

    def add(self, title: str) -> Task:
        # TODO: strip the title, reject empty titles with ValueError,
        #       INSERT with ? parameters, commit, return a Task (cursor.lastrowid is the new id)
        return Task(0, title, "todo")

    def get(self, task_id: int) -> Task | None:
        # TODO: SELECT one row by id; return Task(*row) or None
        return None

    def list(self, status: str | None = None) -> list[Task]:
        # TODO: all tasks ordered by id, or only those with the given status
        return []

    def complete(self, task_id: int) -> bool:
        # TODO: UPDATE the status to 'done', commit, return whether a row changed
        return False


if __name__ == "__main__":
    repo = TaskRepository(sqlite3.connect(":memory:"))
    print(repo.add("  Write tests  "))
    print(repo.add("Ship it"))
    print(repo.complete(1))
    print(repo.list("done"))
    print(repo.list())
    print(repo.get(99))
