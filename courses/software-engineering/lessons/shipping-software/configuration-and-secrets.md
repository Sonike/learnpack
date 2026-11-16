# Configuration and secrets

## Why this matters

The same code runs in several places: your laptop, the CI server, a staging copy and production. Each place needs different settings: a different database, a different port, debug mode on or off. If those settings are written into the code, you have to edit code to deploy, and sooner or later someone commits the production database password to GitHub. Automated bots scan public GitHub for keys around the clock, and a leaked cloud key can be abused within minutes. Getting configuration right is cheap; getting it wrong is one of the most common and expensive junior mistakes.

## Config vs code

**Configuration** is everything that changes between places your app runs (its **environments**), while the code stays the same. Examples:

- the database address (`sqlite:///dev.db` on your laptop, a Postgres server in production),
- the port the server listens on,
- whether debug mode is on,
- the log level,
- API keys and passwords for other services.

**Code** is the logic: how a discount is calculated, which endpoints exist, what a valid email looks like. That doesn't change between environments.

A good test from The Twelve-Factor App, a short and widely used set of rules for web apps: *could you make the repository public right now without leaking anything?* If the answer is no, config is mixed into your code.

Here's the problem in its usual form:

```python
# app.py: config baked into code (don't do this)
DATABASE_URL = "postgres://admin:Sup3rS3cret@db.example.com/shop"
DEBUG = True
```

To deploy, someone edits this file. To run tests against a different database, someone edits it again. And the password is now in Git history forever.

## Environment variables

The standard fix is to read configuration from **environment variables**: named text values that every process receives from whoever starts it (you met them in the lesson Processes, memory and the operating system). Your laptop, the CI server and the hosting platform can each set them differently, and the code never changes.

In Python they're in `os.environ`, which behaves like a dictionary of strings:

```python
import os

database_url = os.environ["DATABASE_URL"]          # KeyError if not set
debug = os.environ.get("DEBUG", "false")            # default if not set
print(database_url, debug)
```

```bash
$ DATABASE_URL=sqlite:///dev.db python3 app.py
sqlite:///dev.db false
```

Set them for a whole terminal session with `export`:

```bash
$ export DATABASE_URL=sqlite:///dev.db
$ python3 app.py
sqlite:///dev.db false
```

On a hosting platform such as Render you type them into a settings page, and in GitHub Actions you store them as encrypted "secrets". Same code everywhere; different values.

## Everything is a string: parse and validate

Environment variables are always text. `PORT=8000` gives you the string `"8000"`, not the number. `DEBUG=false` gives you the string `"false"`, and that's a trap:

```python
import os

os.environ["DEBUG"] = "false"
if os.environ["DEBUG"]:
    print("debug is ON")   # debug is ON   <- any non-empty string is truthy!
```

So you need to **parse** each value into the right type, and **validate** it (check that it makes sense). The best place to do that is in one function, called once when the program starts:

```python
from dataclasses import dataclass

@dataclass
class Config:
    database_url: str
    port: int = 8000
    debug: bool = False

def parse_bool(raw: str) -> bool:
    value = raw.strip().lower()
    if value in ("true", "1", "yes"):
        return True
    if value in ("false", "0", "no", ""):
        return False
    raise ValueError(f"expected true/false, got {raw!r}")

def load_config(env: dict) -> Config:
    if not env.get("DATABASE_URL"):
        raise ValueError("missing required setting: DATABASE_URL")
    return Config(
        database_url=env["DATABASE_URL"],
        port=int(env.get("PORT", "8000")),
        debug=parse_bool(env.get("DEBUG", "false")),
    )

print(load_config({"DATABASE_URL": "sqlite:///dev.db", "DEBUG": "TRUE"}))
# Config(database_url='sqlite:///dev.db', port=8000, debug=True)
```

Three design choices are worth noticing.

1. **One `Config` object.** The rest of the app receives a `Config` and uses `config.port`, never `os.environ` directly. All the parsing lives in one place, and a typo in a setting name is an `AttributeError` you find immediately, not a silent `None`.
2. **The environment is passed in.** `load_config(env)` takes a plain dict. In production you call `load_config(os.environ)`; in tests you pass a small dict. No test ever has to change real environment variables.
3. **Defaults for the safe, optional things; no defaults for the important ones.** A default port is harmless. A default database URL could silently point production at the wrong database, so it's required.

## Fail fast at startup

If a required setting is missing, you want the program to refuse to start, with a clear message, rather than start and crash on the first request an hour later. This is called **failing fast**.

```bash
$ python3 app.py
ConfigError: missing required setting(s): DATABASE_URL, SECRET_KEY
$ echo $?
1
```

A deploy platform sees the non-zero exit code, marks the deploy as failed and keeps the old version running. Compare that with an app that starts, passes its health check, and then fails every checkout because `PAYMENT_KEY` was empty.

Good error messages name **every** missing setting at once (so you don't fix them one by one) and show the bad value for parse errors: `PORT must be a whole number between 1 and 65535, got 'eighty'`. Never put the value of a *secret* in an error message, though; just its name.

## `.env` files for local development

Typing `export` for ten settings every time you open a terminal gets old. The usual answer is a **`.env` file** in the project folder:

```bash
# .env  (local only, never committed)
DATABASE_URL=sqlite:///dev.db
SECRET_KEY=dev-only-not-secret
DEBUG=true
```

A library such as `python-dotenv` (or your framework, or `uv run --env-file .env`) reads this file and puts the values into the environment when the app starts locally. In production there is no `.env` file; the platform sets real environment variables.

Two rules make this safe:

1. **Add `.env` to `.gitignore` before you create it.** `.gitignore` lists files Git should never track:

   ```bash
   $ echo ".env" >> .gitignore
   $ git status --short
   ?? .gitignore
   ```

   `.env` doesn't appear in `git status`, so it can't be committed by accident with `git add .`.

2. **Commit a `.env.example`** with every setting name and safe placeholder values. New teammates copy it to `.env` and fill it in. It documents what the app needs without exposing anything:

   ```bash
   # .env.example
   DATABASE_URL=sqlite:///dev.db
   SECRET_KEY=change-me
   DEBUG=false
   ```

## What counts as a secret

A **secret** is any value that grants access: passwords, API keys, tokens, private keys, the key used to sign session cookies, database URLs that contain a password. Secrets are configuration with extra rules:

- never in code, never in Git, never in a screenshot or a chat message,
- never in logs (the next lesson shows how to redact them),
- never in error messages or URLs,
- only in environment variables or a dedicated secret store the platform provides,
- different in every environment, so a leaked dev key can't touch production.

Some secrets have recognisable shapes, which is what makes automatic scanning possible. AWS access key IDs start with `AKIA` followed by 16 capital letters or digits. Many AI API keys start with `sk-`. GitHub tokens start with `ghp_`. GitHub itself scans pushes for patterns like these (its "push protection" can block a push containing one), and teams often add their own check as a **pre-commit hook**: a script Git runs before each commit that can refuse the commit. You'll write the core of such a check in the practice exercises.

## If you push a secret: rotate first

Suppose you notice that `config.py` with a real API key went to GitHub ten minutes ago. The instinct is to delete the line and push again. That does almost nothing: the key is still in the Git history, and bots may already have copied it.

The correct order:

1. **Rotate the secret immediately.** Go to the service that issued it, revoke (disable) the old key and create a new one. Once the old key is dead, the leak is harmless. This is the step that matters, and it should take minutes.
2. **Put the new key where it belongs**: an environment variable, not code.
3. **Tell your team or lead.** Leaks happen to experienced engineers too; hiding one is what turns it into an incident. They may need to check the service's logs for misuse.
4. **Then clean up**: remove the value from the code, and if the repository is public, consider rewriting history with a tool built for it (GitHub's docs describe `git filter-repo`). History rewriting is the *last* step, and never a replacement for rotation.

## Common mistakes

**Truthy strings.** `if os.environ.get("DEBUG"):` is true for `"false"`, `"0"` and `"no"`. Always parse booleans explicitly.

**`int()` on a missing value.** `int(os.environ.get("PORT"))` raises `TypeError: int() argument must be a string... not 'NoneType'` when `PORT` isn't set. Give a default string (`os.environ.get("PORT", "8000")`) or check first.

**`KeyError: 'DATABASE_URL'` from deep inside the app.** It means a setting was read lazily, far from startup. Move all reads into `load_config` so the error appears at launch with a helpful message.

**Committing `.env` "just once".** Adding `.env` to `.gitignore` after it has been committed doesn't remove it; Git keeps tracking files it already knows about. Run `git rm --cached .env`, commit, and rotate anything that was in it.

**Default secrets.** `SECRET_KEY = os.environ.get("SECRET_KEY", "dev")` means a misconfigured production server quietly runs with the key `"dev"`. Required secrets get no default.

**Pasting secrets into tools.** An API key pasted into a chat, a forum post or an AI assistant has left your control. Treat it as leaked and rotate it.

> **Try it:** In the practice editor, write `parse_bool` from this lesson and call it with `"TRUE"`, `" no "`, `""` and `"maybe"`. Check that the last one raises a `ValueError` with a message that shows the bad value.

## Recap

- Configuration is whatever changes between environments; code is what stays the same. Keep them apart.
- Read config from environment variables, parse every value into the right type, and validate it, all in one `load_config` function that returns a `Config` object.
- Pass the environment in as a dict so tests don't touch the real one.
- Fail fast at startup with a message that names every missing or invalid setting, but never prints a secret's value.
- Use a git-ignored `.env` locally and commit a `.env.example`.
- Secrets never go in code, Git, logs or chats. If one leaks, rotate it first, then tell someone, then clean up.
