# One function, many notifiers

Your app needs to notify users, sometimes by email and sometimes by SMS. Instead of writing `notify_all_by_email` and `notify_all_by_sms`, write **one** `notify_all` that works with anything that has a `send` method. A `typing.Protocol` describes that shape.

```python
@dataclass
class User:
    name: str
    email: str
    phone: str | None = None

class Notifier(Protocol):
    def send(self, user: User, message: str) -> bool: ...

class EmailNotifier: ...
class SMSNotifier: ...

def notify_all(users: list[User], notifier: Notifier, message: str) -> int: ...
```

`User` and `Notifier` are written for you. You write:

- **`EmailNotifier`**: has an `outbox` attribute, a list that starts empty. `send(user, message)` appends `(user.email, message)` to `outbox` and returns `True`.
- **`SMSNotifier`**: also has an `outbox`. `send(user, message)`:
  - returns `False` and records nothing if `user.phone` is `None`;
  - otherwise appends `(user.phone, text)` where `text` is the message cut to at most **160** characters (the SMS limit), and returns `True`.
- **`notify_all(users, notifier, message)`**: calls `notifier.send(user, message)` for every user and returns how many sends returned `True`.

Neither notifier should inherit from `Notifier`. A Protocol is satisfied by having the right method (duck typing), so `notify_all` must work with *any* object that has a matching `send`, including ones the tests make up.

> These "notifiers" only record messages. That's exactly what a **fake** is: a stand-in you can check in tests. A real one would call an email or SMS service.

## Example

```python
ada = User("Ada", "ada@example.com", "+15550100")
bob = User("Bob", "bob@example.com")         # no phone
sms = SMSNotifier()
notify_all([ada, bob], sms, "Your book is due tomorrow")   # 1
sms.outbox     # [("+15550100", "Your book is due tomorrow")]
```
