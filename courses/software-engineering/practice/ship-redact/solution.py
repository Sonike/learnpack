MASK = "***"
SENSITIVE = ("password", "token", "secret", "authorization", "api_key")


def is_sensitive(key) -> bool:
    """True if the key's name looks like it holds a secret."""
    name = str(key).lower().replace("-", "_")
    return any(word in name for word in SENSITIVE)


def clean(value):
    """Redact inside dicts and lists; leave other values alone."""
    if isinstance(value, dict):
        return redact(value)
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def redact(data: dict) -> dict:
    """Return a copy of data with every sensitive value replaced by MASK."""
    return {key: MASK if is_sensitive(key) else clean(value) for key, value in data.items()}
