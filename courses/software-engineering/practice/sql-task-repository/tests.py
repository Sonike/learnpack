import sqlite3

from solution import Task, TaskRepository


def fresh():
    return TaskRepository(sqlite3.connect(":memory:"))


def test_add_returns_a_task_with_its_new_id():
    repo = fresh()
    got = [repo.add("  Write tests  "), repo.add("Ship it")]
    want = [Task(1, "Write tests", "todo"), Task(2, "Ship it", "todo")]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_get_finds_a_task_or_returns_none():
    repo = fresh()
    repo.add("Write tests")
    got = repo.get(1)
    want = Task(1, "Write tests", "todo")
    assert got == want, f"expected {want!r}, got {got!r}"
    got = repo.get(99)
    assert got is None, f"expected None, got {got!r}"


def test_complete_and_list_by_status():
    repo = fresh()
    for title in ["a", "b", "c"]:
        repo.add(title)
    assert repo.complete(2) is True, "complete(2) should return True"
    assert repo.complete(99) is False, "complete(99) should return False"
    got = repo.list("done")
    want = [Task(2, "b", "done")]
    assert got == want, f"expected {want!r}, got {got!r}"
    got = repo.list("todo")
    want = [Task(1, "a", "todo"), Task(3, "c", "todo")]
    assert got == want, f"expected {want!r}, got {got!r}"
    got = [t.id for t in repo.list()]
    assert got == [1, 2, 3], f"expected {[1, 2, 3]!r}, got {got!r}"


def test_rejects_empty_titles():
    repo = fresh()
    for bad in ["", "   "]:
        try:
            repo.add(bad)
            raised = False
        except ValueError:
            raised = True
        assert raised, f"expected ValueError for title {bad!r}"
    assert repo.list() == [], "an empty title was stored"


def test_survives_sql_injection_in_the_title():
    conn = sqlite3.connect(":memory:")
    repo = TaskRepository(conn)
    evil = "x'); DROP TABLE tasks;--"
    task = repo.add(evil)
    got = repo.get(task.id)
    want = Task(task.id, evil, "todo")
    assert got == want, f"expected {want!r}, got {got!r}"
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
    assert "tasks" in tables, "the tasks table is gone!"


def test_injection_in_the_status_filter_matches_nothing():
    repo = fresh()
    repo.add("a")
    got = repo.list("todo' OR '1'='1")
    assert got == [], f"expected {[]!r}, got {got!r}"


def test_changes_are_committed():
    conn = sqlite3.connect(":memory:")
    repo = TaskRepository(conn)
    repo.add("a")
    repo.complete(1)
    conn.rollback()  # if add/complete forgot to commit, this would undo them
    got = repo.list()
    want = [Task(1, "a", "done")]
    assert got == want, f"expected {want!r}, got {got!r}"
