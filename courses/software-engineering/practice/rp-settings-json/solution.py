import json


def save_settings(path, settings: dict) -> None:
    """Write settings to path as pretty JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def load_settings(path, defaults: dict) -> dict:
    """Saved settings on top of defaults. Missing or broken file -> a copy of defaults."""
    try:
        with open(path, encoding="utf-8") as f:
            saved = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(defaults)

    if not isinstance(saved, dict):
        return dict(defaults)
    return {**defaults, **saved}
