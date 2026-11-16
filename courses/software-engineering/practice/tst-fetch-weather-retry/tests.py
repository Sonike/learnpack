from unittest.mock import Mock, call

from solution import fetch_weather

URL = "https://weather.example.com/today?city=Lagos"


def test_returns_data_on_first_success():
    http_get = Mock(return_value={"temp_c": 31})
    got = fetch_weather("Lagos", http_get)
    assert got == {"temp_c": 31}, f"expected {{'temp_c': 31}}, got {got!r}"
    assert http_get.call_args_list == [call(URL)], f"expected one call with {URL!r}, got {http_get.call_args_list!r}"


def test_retries_after_timeouts():
    http_get = Mock(side_effect=[TimeoutError, TimeoutError, {"temp_c": 31}])
    got = fetch_weather("Lagos", http_get)
    assert got == {"temp_c": 31}, f"expected {{'temp_c': 31}}, got {got!r}"
    assert http_get.call_count == 3, f"expected 3 calls, got {http_get.call_count}"


def test_gives_up_after_three_timeouts():
    http_get = Mock(side_effect=[TimeoutError, TimeoutError, TimeoutError, {"temp_c": 31}])
    try:
        fetch_weather("Lagos", http_get)
    except TimeoutError:
        pass
    else:
        raise AssertionError("after 3 timeouts, fetch_weather should re-raise TimeoutError")
    assert http_get.call_count == 3, f"expected exactly 3 attempts, got {http_get.call_count}"


def test_does_not_retry_other_errors():
    http_get = Mock(side_effect=[ValueError("bad JSON"), {"temp_c": 31}])
    try:
        fetch_weather("Lagos", http_get)
    except ValueError:
        pass
    else:
        raise AssertionError("a ValueError should propagate, not be retried or swallowed")
    assert http_get.call_count == 1, f"expected 1 call (no retry on ValueError), got {http_get.call_count}"


def test_respects_a_custom_attempt_count():
    http_get = Mock(side_effect=[TimeoutError] * 5 + [{"temp_c": 31}])
    got = fetch_weather("Lagos", http_get, attempts=6)
    assert (got, http_get.call_count) == ({"temp_c": 31}, 6), f"expected success on call 6, got {(got, http_get.call_count)!r}"
