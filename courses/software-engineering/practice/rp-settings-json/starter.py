import json


def save_settings(path, settings: dict) -> None:
    """Write settings to path as pretty JSON."""
    # TODO: with open(path, "w", encoding="utf-8") as f: json.dump(settings, f, indent=2)
    pass


def load_settings(path, defaults: dict) -> dict:
    """Saved settings on top of defaults. Missing or broken file -> a copy of defaults."""
    # TODO: try to open and json.load the file
    # TODO: except (FileNotFoundError, json.JSONDecodeError): return dict(defaults)
    # TODO: if what you loaded isn't a dict, return dict(defaults)
    # TODO: otherwise return {**defaults, **saved}
    return dict(defaults)


if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    defaults = {"theme": "light", "font_size": 14}
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "settings.json"
        print("first run:", load_settings(path, defaults))
        save_settings(path, {"theme": "dark"})
        if path.exists():
            print("file now holds:", path.read_text(encoding="utf-8"))
        else:
            print("save_settings didn't create the file yet")
        print("second run:", load_settings(path, defaults))
