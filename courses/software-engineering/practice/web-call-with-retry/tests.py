from solution import call_with_retry


class FakeApi:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return self.responses.pop(0)


def test_returns_success_after_temporary_failures():
    api, waits = FakeApi({"status": 503}, {"status": 429}, {"status": 200, "data": "ok"}), []
    got = call_with_retry(api, sleep=waits.append)
    want = {"status": 200, "data": "ok"}
    assert got == want, f"expected {want!r}, got {got!r}"
    assert waits == [1.0, 2.0], f"expected waits {[1.0, 2.0]!r}, got {waits!r}"


def test_does_not_retry_client_errors():
    for status in (400, 401, 404):
        api, waits = FakeApi({"status": status}, {"status": 200}), []
        got = call_with_retry(api, sleep=waits.append)
        assert got == {"status": status}, f"expected {{'status': {status}}}, got {got!r}"
        assert api.calls == 1 and waits == [], f"{status} should not be retried"


def test_gives_up_after_the_retries_and_returns_the_last_response():
    api, waits = FakeApi(*[{"status": 503, "n": i} for i in range(10)]), []
    got = call_with_retry(api, retries=3, sleep=waits.append, base_delay=0.5)
    assert got == {"status": 503, "n": 3}, f"expected the 4th response, got {got!r}"
    assert api.calls == 4, f"expected 4 calls (1 + 3 retries), got {api.calls}"
    assert waits == [0.5, 1.0, 2.0], f"expected waits {[0.5, 1.0, 2.0]!r}, got {waits!r}"


def test_honours_retry_after():
    api, waits = FakeApi({"status": 429, "retry_after": 30}, {"status": 200}), []
    got = call_with_retry(api, sleep=waits.append)
    assert got == {"status": 200}, f"expected {{'status': 200}}, got {got!r}"
    assert waits == [30], f"expected waits {[30]!r}, got {waits!r}"


def test_zero_retries_means_one_call():
    api, waits = FakeApi({"status": 503}, {"status": 200}), []
    got = call_with_retry(api, retries=0, sleep=waits.append)
    assert got == {"status": 503}, f"expected {{'status': 503}}, got {got!r}"
    assert api.calls == 1 and waits == [], f"expected 1 call and no waits, got {api.calls} calls, waits {waits!r}"
