import sqlite3


class TaskRepository:
    """Stores tasks in SQLite. Every method returns plain Python values."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)"
        )

    def add(self, title: str) -> int:
        cursor = self.conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        return cursor.lastrowid

    def get(self, task_id: int) -> dict | None:
        row = self.conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        return {"id": row[0], "title": row[1], "done": bool(row[2])}

    def list(self) -> list[dict]:
        rows = self.conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
        return [{"id": r[0], "title": r[1], "done": bool(r[2])} for r in rows]

    def complete(self, task_id: int) -> bool:
        cursor = self.conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        return cursor.rowcount == 1


def check_repository(make_repo) -> None:
    """Assert that the repositories make_repo() returns keep every promise in the prompt."""
    repo = make_repo()
    task_id = repo.add("Buy milk")
    got = repo.get(task_id)
    assert got == {"id": task_id, "title": "Buy milk", "done": False}, f"get after add returned {got!r}"
    # TODO: a missing id, list order, complete (only that task!), complete on a missing id,
    #       and that done is a real bool


if __name__ == "__main__":
    check_repository(lambda: TaskRepository(sqlite3.connect(":memory:")))
    print("the correct repository passed your checker")
