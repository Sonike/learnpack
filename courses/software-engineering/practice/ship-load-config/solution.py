from dataclasses import dataclass

REQUIRED = ("DATABASE_URL", "SECRET_KEY")
LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


@dataclass
class Config:
    database_url: str
    secret_key: str
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"


class ConfigError(Exception):
    """Raised when the environment can't produce a valid Config."""


def parse_port(raw: str) -> int:
    if raw.strip().isdigit() and 1 <= int(raw) <= 65535:
        return int(raw)
    raise ConfigError(f"PORT must be a whole number between 1 and 65535, got {raw!r}")


def parse_bool(raw: str) -> bool:
    value = raw.strip().lower()
    if value in ("true", "1", "yes"):
        return True
    if value in ("false", "0", "no", ""):
        return False
    raise ConfigError(f"DEBUG must be true or false, got {raw!r}")


def parse_level(raw: str) -> str:
    level = raw.strip().upper()
    if level in LEVELS:
        return level
    raise ConfigError(f"LOG_LEVEL must be one of {', '.join(LEVELS)}, got {raw!r}")


def load_config(env: dict[str, str]) -> Config:
    """Build a Config from environment-variable strings, or raise ConfigError."""
    missing = [key for key in REQUIRED if not env.get(key)]
    if missing:
        raise ConfigError(f"missing required setting(s): {', '.join(missing)}")

    return Config(
        database_url=env["DATABASE_URL"],
        secret_key=env["SECRET_KEY"],
        port=parse_port(env.get("PORT", "8000")),
        debug=parse_bool(env.get("DEBUG", "false")),
        log_level=parse_level(env.get("LOG_LEVEL", "INFO")),
    )
