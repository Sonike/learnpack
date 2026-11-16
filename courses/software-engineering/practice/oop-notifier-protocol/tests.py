from solution import EmailNotifier, Notifier, SMSNotifier, User, notify_all

ADA = User("Ada", "ada@example.com", "+15550100")
BOB = User("Bob", "bob@example.com")


def test_email_notifier_sends_to_everyone():
    email = EmailNotifier()
    got = notify_all([ADA, BOB], email, "Due tomorrow")
    assert got == 2, f"expected 2, got {got!r}"
    want = [("ada@example.com", "Due tomorrow"), ("bob@example.com", "Due tomorrow")]
    assert email.outbox == want, f"expected {want!r}, got {email.outbox!r}"


def test_sms_notifier_skips_users_without_a_phone():
    sms = SMSNotifier()
    got = notify_all([ADA, BOB], sms, "Due tomorrow")
    assert got == 1, f"expected 1, got {got!r}"
    assert sms.outbox == [("+15550100", "Due tomorrow")], f"got {sms.outbox!r}"


def test_sms_is_cut_to_160_characters():
    sms = SMSNotifier()
    sms.send(ADA, "x" * 200)
    got = len(sms.outbox[0][1])
    assert got == 160, f"expected 160 characters, got {got!r}"


def test_works_with_any_object_that_has_send():
    class AlwaysFails:
        def send(self, user, message):
            return False

    class Recorder:
        def __init__(self):
            self.names = []

        def send(self, user, message):
            self.names.append(user.name)
            return True

    assert notify_all([ADA, BOB], AlwaysFails(), "hi") == 0, "a notifier whose sends fail should count 0"
    recorder = Recorder()
    got = notify_all([ADA, BOB], recorder, "hi")
    assert (got, recorder.names) == (2, ["Ada", "Bob"]), f"expected (2, ['Ada', 'Bob']), got {(got, recorder.names)!r}"


def test_no_users_sends_nothing():
    email = EmailNotifier()
    got = notify_all([], email, "hi")
    assert (got, email.outbox) == (0, []), f"expected (0, []), got {(got, email.outbox)!r}"


def test_notifiers_do_not_inherit_from_the_protocol():
    for cls in (EmailNotifier, SMSNotifier):
        assert Notifier not in cls.__mro__, f"{cls.__name__} shouldn't inherit from Notifier: a Protocol is matched by shape"
