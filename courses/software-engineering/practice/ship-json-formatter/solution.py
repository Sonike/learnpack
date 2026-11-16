import json
import logging
from datetime import datetime, timezone

# Attribute names every LogRecord has. Anything else came from extra={...}.
STANDARD = set(logging.LogRecord("x", logging.INFO, "", 0, "", None, None).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """Return the record as one line of JSON."""
        data = {
            "time": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in STANDARD:
                data[key] = value
        if record.exc_info:
            data["exception"] = self.formatException(record.exc_info)
        return json.dumps(data, default=str)
