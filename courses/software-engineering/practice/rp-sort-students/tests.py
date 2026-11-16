from solution import sort_students


def names(records):
    return [r["name"] for r in records]


def test_highest_grade_comes_first():
    got = names(sort_students([{"name": "B", "grade": 70}, {"name": "A", "grade": 95}, {"name": "C", "grade": 80}]))
    want = ["A", "C", "B"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_equal_grades_are_sorted_by_name():
    records = [{"name": "Grace", "grade": 85}, {"name": "Ada", "grade": 91}, {"name": "Alan", "grade": 85}]
    got = names(sort_students(records))
    want = ["Ada", "Alan", "Grace"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_identical_grade_and_name_keep_their_order():
    records = [{"name": "Sam", "grade": 80, "id": 2}, {"name": "Sam", "grade": 80, "id": 1}, {"name": "Ann", "grade": 80, "id": 3}]
    got = [r["id"] for r in sort_students(records)]
    want = [3, 2, 1]
    assert got == want, f"expected ids {want!r} (the two Sams in their original order), got {got!r}"


def test_does_not_change_the_input():
    records = [{"name": "B", "grade": 1}, {"name": "A", "grade": 2}]
    snapshot = [dict(r) for r in records]
    sort_students(records)
    assert records == snapshot, f"the original list should be untouched, got {records!r}"


def test_empty_list():
    got = sort_students([])
    assert got == [], f"expected [], got {got!r}"
