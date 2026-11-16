import io
import json
import logging
from datetime import datetime, timezone

# Attribute names every LogRecord has. Anything else came from extra={...}.
STANDARD = set(logging.LogRecord("x", logging.INFO, "", 0, "", None, None).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """Return the record as one line of JSON."""
        # TODO: build a dict with time, level, logger, message
        # TODO: add every key in record.__dict__ that isn't in STANDARD
        # TODO: add "exception" if record.exc_info is set
        # TODO: return json.dumps(data, default=str)
        return "{}"


if __name__ == "__main__":
    buffer = io.StringIO()
    handler = logging.StreamHandler(buffer)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("shop.orders")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    logger.info("order %s paid", 1093, extra={"user_id": 77, "total": 49.9})
    print(buffer.getvalue())
