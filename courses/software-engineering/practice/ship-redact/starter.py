MASK = "***"
SENSITIVE = ("password", "token", "secret", "authorization", "api_key")


def is_sensitive(key) -> bool:
    """True if the key's name looks like it holds a secret."""
    # TODO: lower-case, replace "-" with "_", check if any SENSITIVE word is in it
    return False


def redact(data: dict) -> dict:
    """Return a copy of data with every sensitive value replaced by MASK."""
    # TODO: build a new dict; mask sensitive keys; recurse into dicts and lists
    return data


if __name__ == "__main__":
    request = {
        "user": "ada",
        "password": "hunter2",
        "headers": {"Authorization": "Bearer abc", "Accept": "json"},
        "items": [{"sku": 1, "api_key": "k"}],
    }
    print(redact(request))
    print(request["password"])   # the original must still say hunter2
