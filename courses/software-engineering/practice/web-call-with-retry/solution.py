import time

RETRYABLE = {429, 503}


def call_with_retry(fn, retries: int = 3, sleep=time.sleep, base_delay: float = 1.0) -> dict:
    """Call fn(), retrying 429/503 responses with exponential backoff."""
    for attempt in range(retries + 1):
        response = fn()
        if response["status"] not in RETRYABLE or attempt == retries:
            return response
        sleep(response.get("retry_after", base_delay * 2 ** attempt))
    return response  # only reached when retries < 0


if __name__ == "__main__":
    responses = iter([{"status": 503}, {"status": 429}, {"status": 200, "data": "ok"}])
    waits = []
    print(call_with_retry(lambda: next(responses), sleep=waits.append))
    print("waited:", waits)
