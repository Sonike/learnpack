import json
import tempfile
from pathlib import Path

from solution import load_settings, save_settings

DEFAULTS = {"theme": "light", "font_size": 14}


def test_missing_file_returns_the_defaults():
    with tempfile.TemporaryDirectory() as folder:
        got = load_settings(Path(folder) / "nope.json", DEFAULTS)
    assert got == DEFAULTS, f"expected {DEFAULTS!r}, got {got!r}"


def test_save_then_load_round_trips():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "settings.json"
        save_settings(path, {"theme": "dark", "font_size": 18})
        got = load_settings(path, DEFAULTS)
    want = {"theme": "dark", "font_size": 18}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_saved_file_is_pretty_json():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "settings.json"
        save_settings(path, {"theme": "dark"})
        text = path.read_text(encoding="utf-8")
    assert json.loads(text) == {"theme": "dark"}, f"the file should hold the settings as JSON, got {text!r}"
    assert "\n  " in text, f"use indent=2 so people can read the file, got {text!r}"


def test_saved_values_override_defaults_and_new_defaults_are_kept():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "settings.json"
        save_settings(path, {"theme": "dark"})
        got = load_settings(path, DEFAULTS)
    want = {"theme": "dark", "font_size": 14}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_corrupt_or_wrong_shaped_file_returns_the_defaults():
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "settings.json"
        for text in ['{"theme": "dark",', "", "[1, 2]"]:
            path.write_text(text, encoding="utf-8")
            got = load_settings(path, DEFAULTS)
            assert got == DEFAULTS, f"file containing {text!r}: expected {DEFAULTS!r}, got {got!r}"


def test_defaults_are_never_changed():
    defaults = {"theme": "light"}
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "settings.json"
        result = load_settings(path, defaults)
        result["theme"] = "changed by caller"
        save_settings(path, {"theme": "dark"})
        load_settings(path, defaults)
    assert defaults == {"theme": "light"}, f"load_settings must not change defaults, got {defaults!r}"
