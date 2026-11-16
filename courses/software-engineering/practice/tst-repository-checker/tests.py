import sqlite3

from solution import check_repository


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


class WrongOrder(TaskRepository):
    def list(self):
        return list(reversed(super().list()))


class CompletesEverything(TaskRepository):
    def complete(self, task_id):
        exists = self.get(task_id) is not None
        self.conn.execute("UPDATE tasks SET done = 1")  # forgot the WHERE clause
        return exists


class CompleteAlwaysTrue(TaskRepository):
    def complete(self, task_id):
        super().complete(task_id)
        return True


class GetMissingRaises(TaskRepository):
    def get(self, task_id):
        row = self.conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return {"id": row[0], "title": row[1], "done": bool(row[2])}  # crashes when row is None


class DoneAsInt(TaskRepository):
    def get(self, task_id):
        row = self.conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return None if row is None else {"id": row[0], "title": row[1], "done": row[2]}


def maker(cls):
    return lambda: cls(sqlite3.connect(":memory:"))


def caught(cls):
    try:
        check_repository(maker(cls))
    except Exception:
        return True
    return False


def test_correct_repository_passes():
    try:
        check_repository(maker(TaskRepository))
    except AssertionError as e:
        raise AssertionError(f"your checker rejected the correct repository: {e}") from None


def test_catches_list_in_the_wrong_order():
    assert caught(WrongOrder), "missed a repository whose list() returns tasks newest-first"


def test_catches_complete_that_updates_every_row():
    assert caught(CompletesEverything), "missed a repository whose complete() marks every task done (add two tasks, complete one)"


def test_catches_complete_returning_true_for_missing_id():
    assert caught(CompleteAlwaysTrue), "missed a repository whose complete(999) returns True"


def test_catches_get_crashing_on_missing_id():
    assert caught(GetMissingRaises), "missed a repository whose get(999) crashes instead of returning None"


def test_catches_done_stored_as_an_int():
    assert caught(DoneAsInt), "missed a repository that returns done as 0/1 instead of False/True"
