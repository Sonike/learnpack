from datetime import datetime
from unittest.mock import Mock, call

from solution import send_reminders

NOW = datetime(2026, 11, 13, 9, 0)


def task(title, owner, due, done=False):
    return {"title": title, "owner": owner, "due": due, "done": done}


def test_sends_one_reminder_per_overdue_task():
    mailer = Mock()
    tasks = [
        task("Pay rent", "ada@example.com", datetime(2026, 11, 1)),
        task("Book dentist", "bob@example.com", datetime(2026, 12, 1)),
        task("Renew passport", "bob@example.com", datetime(2026, 11, 12)),
    ]
    got = send_reminders(tasks, NOW, mailer)
    want = [call("ada@example.com", "Overdue: Pay rent"), call("bob@example.com", "Overdue: Renew passport")]
    assert mailer.send.call_args_list == want, f"expected {want!r}, got {mailer.send.call_args_list!r}"
    assert got == 2, f"expected 2, got {got!r}"


def test_done_tasks_are_skipped():
    mailer = Mock()
    got = send_reminders([task("Pay rent", "ada@example.com", datetime(2026, 11, 1), done=True)], NOW, mailer)
    assert (got, mailer.send.call_count) == (0, 0), f"expected no reminders for a done task, got {got} and {mailer.send.call_args_list!r}"


def test_task_due_exactly_now_is_not_overdue():
    mailer = Mock()
    got = send_reminders([task("Stand-up", "ada@example.com", NOW)], NOW, mailer)
    assert (got, mailer.send.call_count) == (0, 0), f"a task due exactly now is not overdue yet, got {mailer.send.call_args_list!r}"


def test_uses_the_given_now_not_the_real_clock():
    mailer = Mock()
    far_past = datetime(2000, 1, 1)
    got = send_reminders([task("Pay rent", "ada@example.com", datetime(2026, 11, 1))], far_past, mailer)
    assert got == 0, f"with now = 2000-01-01, a task due in 2026 is not overdue; got {got!r}. Use the now argument, not datetime.now()"


def test_no_tasks_sends_nothing():
    mailer = Mock()
    got = send_reminders([], NOW, mailer)
    assert (got, mailer.send.call_count) == (0, 0), f"expected (0, 0), got {(got, mailer.send.call_count)!r}"
