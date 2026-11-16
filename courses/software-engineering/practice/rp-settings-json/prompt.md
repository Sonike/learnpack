# Save and load settings as JSON

Apps remember your settings between runs by saving them to a file. The file might not exist yet (first run), or it might be broken (someone edited it by hand). In both cases the app should start with sensible defaults, not crash.

```python
def save_settings(path, settings: dict) -> None:
def load_settings(path, defaults: dict) -> dict:
```

- `save_settings` writes `settings` to `path` as JSON with `indent=2`, using `encoding="utf-8"`.
- `load_settings` reads the JSON file at `path` and returns the settings:
  - Start from the defaults and let the saved values override them: `{**defaults, **saved}`. That way a setting added in a newer version of the app still has a value.
  - If the file doesn't exist (`FileNotFoundError`) or isn't valid JSON (`json.JSONDecodeError`), return a **copy** of `defaults`.
  - If the file holds valid JSON that isn't an object (e.g. `[1, 2]`), also return a copy of `defaults`.
  - Never change the `defaults` dict you were given.

## Example

```python
defaults = {"theme": "light", "font_size": 14}
load_settings("settings.json", defaults)              # {"theme": "light", "font_size": 14}  (no file yet)
save_settings("settings.json", {"theme": "dark"})
load_settings("settings.json", defaults)              # {"theme": "dark", "font_size": 14}
```
