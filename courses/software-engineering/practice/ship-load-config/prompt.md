# Load and validate configuration

Write the one function every service needs: turn raw environment variables (all strings) into a typed, validated `Config`, and refuse to start with a clear message if something is wrong.

```python
@dataclass
class Config:
    database_url: str
    secret_key: str
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"

class ConfigError(Exception): ...

def load_config(env: dict[str, str]) -> Config:
```

`env` is a dictionary of setting names to string values, like `os.environ`. (Tests pass a small dict; in a real app you'd call `load_config(os.environ)`.)

## Rules

1. **Required:** `DATABASE_URL` and `SECRET_KEY`. A key that's missing **or empty** counts as missing. If any are missing, raise `ConfigError` with the message `missing required setting(s): ` followed by the missing names, in that order, joined with `", "`. Check this first.
2. **`PORT`** (optional, default `8000`): must be a whole number from 1 to 65535. Otherwise raise `ConfigError(f"PORT must be a whole number between 1 and 65535, got {raw!r}")`.
3. **`DEBUG`** (optional, default `False`): ignoring case and surrounding spaces, `"true"`, `"1"`, `"yes"` mean `True`; `"false"`, `"0"`, `"no"` and `""` mean `False`. Anything else: `ConfigError(f"DEBUG must be true or false, got {raw!r}")`.
4. **`LOG_LEVEL`** (optional, default `"INFO"`): converted to upper case; must be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Otherwise `ConfigError(f"LOG_LEVEL must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL, got {raw!r}")`.
5. Ignore any other keys in `env`.

> **Note:** never include `SECRET_KEY`'s value in an error message. The rules above only ever show the values of non-secret settings.

## Example

```python
load_config({"DATABASE_URL": "sqlite:///dev.db", "SECRET_KEY": "x", "PORT": "5000", "DEBUG": " Yes "})
# Config(database_url='sqlite:///dev.db', secret_key='x', port=5000, debug=True, log_level='INFO')

load_config({"PORT": "5000"})
# ConfigError: missing required setting(s): DATABASE_URL, SECRET_KEY
```
