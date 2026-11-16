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
    # add + get
    repo = make_repo()
    milk = repo.add("Buy milk")
    got = repo.get(milk)
    assert got == {"id": milk, "title": "Buy milk", "done": False}, f"get after add returned {got!r}"
    assert got["done"] is False, f"done should be the bool False, got {got['done']!r}"

    # a missing id
    assert repo.get(999) is None, "get on a missing id should return None"

    # list keeps insertion order
    repo = make_repo()
    ids = [repo.add(title) for title in ["a", "b", "c"]]
    got = [(t["id"], t["title"]) for t in repo.list()]
    assert got == list(zip(ids, ["a", "b", "c"])), f"list should return tasks in the order added, got {got!r}"

    # complete only touches one task
    repo = make_repo()
    first, second = repo.add("first"), repo.add("second")
    assert repo.complete(first) is True, "complete on an existing task should return True"
    assert repo.get(first)["done"] is True, "the completed task should be done"
    assert repo.get(second)["done"] is False, "completing one task must not complete the others"

    # complete on a missing id
    assert repo.complete(999) is False, "complete on a missing id should return False"


if __name__ == "__main__":
    check_repository(lambda: TaskRepository(sqlite3.connect(":memory:")))
    print("the correct repository passed your checker")
