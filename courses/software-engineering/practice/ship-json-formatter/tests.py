import io
import json
import logging
from datetime import date

from solution import JsonFormatter


def make_logger(name):
    buffer = io.StringIO()
    handler = logging.StreamHandler(buffer)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger(name)
    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger, buffer


def lines(buffer):
    return [json.loads(line) for line in buffer.getvalue().splitlines()]


def test_writes_one_json_object_per_line():
    logger, buffer = make_logger("t.one")
    logger.info("first")
    logger.warning("second")
    got = [(d["level"], d["message"]) for d in lines(buffer)]
    want = [("INFO", "first"), ("WARNING", "second")]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_has_time_level_logger_and_message_first():
    logger, buffer = make_logger("shop.orders")
    logger.info("order %s paid", 1093)
    record = lines(buffer)[0]
    got = list(record)[:4]
    want = ["time", "level", "logger", "message"]
    assert got == want, f"expected {want!r}, got {got!r}"
    got = (record["logger"], record["message"], record["time"].endswith("+00:00"))
    want = ("shop.orders", "order 1093 paid", True)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_includes_extra_fields():
    logger, buffer = make_logger("t.extra")
    logger.info("paid", extra={"user_id": 77, "total": 49.9})
    record = lines(buffer)[0]
    got = {k: record[k] for k in record if k not in ("time", "level", "logger", "message")}
    want = {"user_id": 77, "total": 49.9}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_unusual_values_become_strings_instead_of_crashing():
    logger, buffer = make_logger("t.date")
    logger.info("report", extra={"day": date(2026, 11, 13)})
    got = lines(buffer)[0]["day"]
    want = "2026-11-13"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_adds_traceback_only_for_exceptions():
    logger, buffer = make_logger("t.exc")
    logger.info("fine")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("boom")
    plain, failed = lines(buffer)
    got = ("exception" in plain, "ZeroDivisionError" in failed.get("exception", ""))
    want = (False, True)
    assert got == want, f"expected {want!r}, got {got!r}"
