from datetime import datetime


def send_reminders(tasks: list[dict], now: datetime, mailer) -> int:
    """Email the owner of every overdue, unfinished task. Return the number sent."""
    # TODO: overdue = not done and due < now; call mailer.send(owner, "Overdue: " + title)
    return 0


if __name__ == "__main__":
    from unittest.mock import Mock

    mailer = Mock()
    now = datetime(2026, 11, 13, 9, 0)
    tasks = [
        {"title": "Pay rent", "owner": "ada@example.com", "due": datetime(2026, 11, 1), "done": False},
        {"title": "Book dentist", "owner": "bob@example.com", "due": datetime(2026, 12, 1), "done": False},
    ]
    print("sent", send_reminders(tasks, now, mailer))
    print(mailer.send.call_args_list)
