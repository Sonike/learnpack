BASE_URL = "https://weather.example.com/today?city="


def fetch_weather(city: str, http_get, attempts: int = 3) -> dict:
    """Return http_get(url), retrying on TimeoutError up to `attempts` calls in total."""
    # TODO: loop up to attempts times; return on success; on TimeoutError try again;
    #       after the last failed attempt, re-raise
    return {}


if __name__ == "__main__":
    from unittest.mock import Mock

    http_get = Mock(side_effect=[TimeoutError, TimeoutError, {"temp_c": 31}])
    print(fetch_weather("Lagos", http_get), "after", http_get.call_count, "calls")
