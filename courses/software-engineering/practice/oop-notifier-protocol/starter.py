from dataclasses import dataclass
from typing import Protocol


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
        # TODO: record (user.email, message) and return True
        return False


class SMSNotifier:
    def __init__(self):
        self.outbox: list[tuple[str, str]] = []

    def send(self, user: User, message: str) -> bool:
        # TODO: no phone -> False. Otherwise record (phone, first 160 chars) and return True
        return False


def notify_all(users: list[User], notifier: Notifier, message: str) -> int:
    """Send message to every user; return how many sends succeeded."""
    # TODO
    return 0


if __name__ == "__main__":
    ada = User("Ada", "ada@example.com", "+15550100")
    bob = User("Bob", "bob@example.com")
    email, sms = EmailNotifier(), SMSNotifier()
    print(notify_all([ada, bob], email, "Your book is due tomorrow"), email.outbox)
    print(notify_all([ada, bob], sms, "Your book is due tomorrow"), sms.outbox)
