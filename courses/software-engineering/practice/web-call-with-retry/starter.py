import time

RETRYABLE = {429, 503}


def call_with_retry(fn, retries: int = 3, sleep=time.sleep, base_delay: float = 1.0) -> dict:
    """Call fn(), retrying 429/503 responses with exponential backoff."""
    # TODO: loop over attempts 0..retries, return early for non-retryable statuses,
    #       sleep base_delay * 2 ** attempt (or retry_after) between attempts
    return fn()


if __name__ == "__main__":
    responses = iter([{"status": 503}, {"status": 429}, {"status": 200, "data": "ok"}])
    waits = []
    print(call_with_retry(lambda: next(responses), sleep=waits.append))
    print("waited:", waits)
