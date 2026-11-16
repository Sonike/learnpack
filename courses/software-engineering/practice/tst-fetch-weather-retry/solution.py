BASE_URL = "https://weather.example.com/today?city="


def fetch_weather(city: str, http_get, attempts: int = 3) -> dict:
    """Return http_get(url), retrying on TimeoutError up to `attempts` calls in total."""
    url = BASE_URL + city
    for attempt in range(1, attempts + 1):
        try:
            return http_get(url)
        except TimeoutError:
            if attempt == attempts:
                raise


if __name__ == "__main__":
    from unittest.mock import Mock

    http_get = Mock(side_effect=[TimeoutError, {"temp_c": 31}])
    print(fetch_weather("Lagos", http_get), http_get.call_count)
