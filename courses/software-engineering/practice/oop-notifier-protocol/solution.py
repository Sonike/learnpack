from dataclasses import dataclass
from typing import Protocol

SMS_LIMIT = 160


@dataclass
class User:
    name: str
    email: str
    phone: str | None = None


class Notifier(Protocol):
    def send(self, user: User, message: str) -> bool: ...


class EmailNotifier:
    def __init__(self):
        self.outbox: list[tuple[str, str]] = []

    def send(self, user: User, message: str) -> bool:
        self.outbox.append((user.email, message))
        return True


class SMSNotifier:
    def __init__(self):
        self.outbox: list[tuple[str, str]] = []

    def send(self, user: User, message: str) -> bool:
        if user.phone is None:
            return False
        self.outbox.append((user.phone, message[:SMS_LIMIT]))
        return True


def notify_all(users: list[User], notifier: Notifier, message: str) -> int:
    """Send message to every user; return how many sends succeeded."""
    return sum(1 for user in users if notifier.send(user, message))


if __name__ == "__main__":
    sms = SMSNotifier()
    print(notify_all([User("Ada", "ada@example.com", "+15550100")], sms, "Hi"), sms.outbox)
