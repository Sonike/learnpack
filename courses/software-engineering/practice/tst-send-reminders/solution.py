from datetime import datetime


def is_overdue(task: dict, now: datetime) -> bool:
    return not task["done"] and task["due"] < now


def send_reminders(tasks: list[dict], now: datetime, mailer) -> int:
    """Email the owner of every overdue, unfinished task. Return the number sent."""
    overdue = [task for task in tasks if is_overdue(task, now)]
    for task in overdue:
        mailer.send(task["owner"], "Overdue: " + task["title"])
    return len(overdue)


if __name__ == "__main__":
    from unittest.mock import Mock

    mailer = Mock()
    print(send_reminders([{"title": "Pay rent", "owner": "ada@example.com", "due": datetime(2026, 11, 1), "done": False}], datetime(2026, 11, 13), mailer))
    print(mailer.send.call_args_list)
