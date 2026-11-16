from solution import Config, ConfigError, load_config

BASE = {"DATABASE_URL": "sqlite:///dev.db", "SECRET_KEY": "s3cret"}


def error_message(env):
    try:
        load_config(env)
    except ConfigError as e:
        return str(e)
    return None


def test_uses_defaults_for_optional_settings():
    got = load_config(dict(BASE))
    want = Config("sqlite:///dev.db", "s3cret", 8000, False, "INFO")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_parses_port_debug_and_log_level():
    env = dict(BASE, PORT="5000", DEBUG=" Yes ", LOG_LEVEL="warning", EXTRA="ignored")
    got = load_config(env)
    want = Config("sqlite:///dev.db", "s3cret", 5000, True, "WARNING")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_debug_false_string_is_false():
    got = load_config(dict(BASE, DEBUG="false")).debug
    assert got is False, f"expected False, got {got!r}"


def test_reports_every_missing_or_empty_required_setting():
    got = error_message({"SECRET_KEY": "", "PORT": "5000"})
    want = "missing required setting(s): DATABASE_URL, SECRET_KEY"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_rejects_bad_port_with_the_bad_value_in_the_message():
    for raw in ("eighty", "0", "70000", "-1"):
        got = error_message(dict(BASE, PORT=raw))
        want = f"PORT must be a whole number between 1 and 65535, got {raw!r}"
        assert got == want, f"expected {want!r}, got {got!r}"


def test_rejects_unknown_debug_and_log_level_values():
    got = error_message(dict(BASE, DEBUG="maybe"))
    want = "DEBUG must be true or false, got 'maybe'"
    assert got == want, f"expected {want!r}, got {got!r}"
    got = error_message(dict(BASE, LOG_LEVEL="loud"))
    want = "LOG_LEVEL must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL, got 'loud'"
    assert got == want, f"expected {want!r}, got {got!r}"
