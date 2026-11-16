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
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id     INTEGER PRIMARY KEY,
                    title  TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'todo'
                )
                """
            )

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        with self.conn:
            cur = self.conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        return Task(cur.lastrowid, title, "todo")

    def get(self, task_id: int) -> Task | None:
        row = self.conn.execute(
            "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return Task(*row) if row else None

    def list(self, status: str | None = None) -> list[Task]:
        if status is None:
            rows = self.conn.execute("SELECT id, title, status FROM tasks ORDER BY id")
        else:
            rows = self.conn.execute(
                "SELECT id, title, status FROM tasks WHERE status = ? ORDER BY id", (status,)
            )
        return [Task(*row) for row in rows]

    def complete(self, task_id: int) -> bool:
        with self.conn:
            cur = self.conn.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
        return cur.rowcount == 1


if __name__ == "__main__":
    repo = TaskRepository(sqlite3.connect(":memory:"))
    repo.add("Write tests")
    repo.complete(1)
    print(repo.list())
