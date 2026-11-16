from solution import Status, Task, TaskList


def test_add_gives_increasing_ids():
    tasks = TaskList()
    first = tasks.add("Buy milk")
    second = tasks.add("Write tests")
    want = [Task(1, "Buy milk", Status.TODO), Task(2, "Write tests", Status.TODO)]
    assert [first, second] == want, f"expected {want!r}, got {[first, second]!r}"


def test_complete_marks_task_done():
    tasks = TaskList()
    tasks.add("Buy milk")
    got = tasks.complete(1)
    assert got.status is Status.DONE, f"expected Status.DONE, got {got.status!r}"


def test_by_status_filters_in_order():
    tasks = TaskList()
    for title in ["a", "b", "c", "d"]:
        tasks.add(title)
    tasks.complete(3)
    tasks.complete(1)
    got = [t.title for t in tasks.by_status(Status.DONE)]
    assert got == ["a", "c"], f"expected ['a', 'c'], got {got!r}"
    got = [t.title for t in tasks.by_status(Status.TODO)]
    assert got == ["b", "d"], f"expected ['b', 'd'], got {got!r}"


def test_by_status_on_empty_list_is_empty():
    got = TaskList().by_status(Status.TODO)
    assert got == [], f"expected [], got {got!r}"


def test_completing_unknown_id_raises_key_error():
    tasks = TaskList()
    tasks.add("Buy milk")
    try:
        tasks.complete(99)
    except KeyError:
        return
    raise AssertionError("complete(99) should raise KeyError")


def test_rejects_empty_title():
    try:
        TaskList().add("   ")
    except ValueError:
        return
    raise AssertionError("add('   ') should raise ValueError")
