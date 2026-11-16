from dataclasses import dataclass


@dataclass
class Config:
    database_url: str
    secret_key: str
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"


class ConfigError(Exception):
    """Raised when the environment can't produce a valid Config."""


def load_config(env: dict[str, str]) -> Config:
    """Build a Config from environment-variable strings, or raise ConfigError."""
    # TODO: collect missing required keys (missing or empty) and raise one ConfigError
    # TODO: parse PORT (int, 1..65535)
    # TODO: parse DEBUG (true/1/yes, false/0/no/"")
    # TODO: parse LOG_LEVEL (upper-case, one of the five levels)
    return Config(database_url="", secret_key="")


if __name__ == "__main__":
    print(load_config({"DATABASE_URL": "sqlite:///dev.db", "SECRET_KEY": "x", "DEBUG": "yes"}))
    try:
        load_config({})
    except ConfigError as e:
        print("ConfigError:", e)
