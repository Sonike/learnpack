# Packaging, CI and deploying

## Why this matters

"It works on my machine" is the most famous sentence in software, and it's never a good one. Your laptop has a particular Python version, a particular set of installed packages and a dozen settings you've forgotten about. A teammate's laptop, the CI server and the production server have different ones. This lesson is about making your project reproducible (anyone can install exactly what it needs), checked automatically on every change (CI), and put in front of users safely (deploying), with a way back when something goes wrong (rollback). These are the skills that turn a project on GitHub into a running service, and they're among the first things a hiring manager checks in a portfolio.

## Describing your project: `pyproject.toml`

A Python project describes itself in a file called **`pyproject.toml`** at the root of the repository. **TOML** is a simple settings format: `[sections]` in square brackets and `key = value` lines.

```toml
[project]
name = "habit-api"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn>=0.30",
]

[dependency-groups]
dev = [
    "pytest>=8",
    "ruff>=0.6",
]
```

What each part means:

- `name` and `version`: what the project is called and which release this is.
- `requires-python`: the Python versions it supports. Installers refuse to install it on older ones, which is far better than a confusing `SyntaxError` later.
- `dependencies`: the packages the app needs to **run**. `>=0.115` is a **version constraint**: "0.115 or newer".
- `[dependency-groups]`: packages only developers need, such as the test runner and the linter. They aren't installed on the production server.

Python can read TOML itself with the standard `tomllib` module (Python 3.11+):

```python
import tomllib

text = '''
[project]
name = "habit-api"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115"]
'''
data = tomllib.loads(text)
print(data["project"]["requires-python"])   # >=3.12
print(data["project"]["dependencies"])      # ['fastapi>=0.115']
```

The first practice exercise uses `tomllib` to write a small checker for these files.

## Lockfiles: the exact versions

`fastapi>=0.115` allows any newer version. That's what you want when you *choose* to upgrade, and not what you want when a new release quietly appears between your test run and your deploy. So tools also write a **lockfile**: a generated file listing the **exact** version of every package, including the dependencies of your dependencies.

```
pyproject.toml  -> what you asked for     "fastapi>=0.115"
uv.lock         -> what was actually chosen  fastapi 0.115.4, starlette 0.41.2, pydantic 2.9.2, ...
```

You commit the lockfile. Then your laptop, CI and production install identical versions, and "works on my machine" mostly goes away.

## Two ways to install: pip and uv

You already know the classic way from the setup lessons:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install fastapi pytest
```

That's what most documentation and Stack Overflow answers assume, so you need to know it. Many teams now use **uv**, a much faster tool from Astral that manages the virtual environment, the dependencies and the lockfile together:

```bash
$ uv init habit-api          # creates pyproject.toml
$ cd habit-api
$ uv add fastapi             # adds to dependencies, updates uv.lock, installs
$ uv add --dev pytest ruff   # adds to the dev group
$ uv run pytest              # runs inside the project's environment
========================= 12 passed in 0.41s =========================
$ uv sync                    # on another machine: install exactly what uv.lock says
```

Either works. What matters is the idea: dependencies are written down, versions are locked, and one command reproduces the environment.

## Continuous integration (CI)

**Continuous integration** means that every push and every pull request is automatically checked on a clean machine. You set this up in the testing section with GitHub Actions; now let's look at the whole **pipeline**, the ordered list of stages a change passes through:

```
 push / PR
    |
    v
 [1 install] -> [2 lint] -> [3 test] -> [4 build] -> [5 deploy]
                 ruff        pytest      (image or     main branch
                 check                    package)     only
```

The order is deliberate: **cheapest and fastest checks first**. Linting takes seconds and catches typos and unused imports; there's no point running a five-minute test suite on code that doesn't even pass the linter. And any failing stage **stops the pipeline**: a stage fails when its command exits with a non-zero code (the exit codes from the first lesson of this section).

A minimal GitHub Actions workflow, `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run pytest
```

Pair this with a **branch protection rule** on `main` ("require the CI check to pass before merging") and broken code can't reach `main` without someone deliberately overriding it.

## Environments: dev, staging, production

An **environment** is one place your app runs, with its own config and data:

- **Development (dev):** your laptop. Debug on, a throwaway SQLite file, fake keys.
- **Staging:** a copy of production that real users don't see. You deploy here first and click through the important flows.
- **Production (prod):** the real thing, with real users and real data.

Same code, different configuration, exactly as the lesson Configuration and secrets described. Keeping the environments as similar as possible (same Python version, same database type) is what makes "it worked in staging" mean something.

## Deploying to a platform

**Deploying** means getting a new version of your code running where users can reach it. As a junior, the easiest route is a **PaaS** (platform as a service) such as Render or PythonAnywhere: you connect your GitHub repository, tell it how to install and start your app, set environment variables in its dashboard, and it handles the servers.

For a FastAPI app on Render, the settings boil down to:

```
Build command:  pip install -r requirements.txt     (or: uv sync)
Start command:  uvicorn app.main:app --host 0.0.0.0 --port $PORT
Environment:    DATABASE_URL=...  SECRET_KEY=...  LOG_LEVEL=INFO
```

Two details matter. `--host 0.0.0.0` makes the server listen for connections from outside the machine (the default, `127.0.0.1`, only accepts connections from itself). And `$PORT` is set by the platform, which is why your app reads its port from config.

## Health checks and rollbacks

A **health check** is a tiny endpoint, usually `GET /health`, that returns `200 OK` when the app is working:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

The platform calls it after starting a new version. If it doesn't answer with 200, the platform keeps the old version running and marks the deploy as failed. A good health check also confirms the app can reach the things it truly needs, such as the database, but stays fast.

A **rollback** is going back to the previous working version. Every deploy will eventually go wrong, so you want a rollback to be boring: on most platforms it's one click ("redeploy previous"), or a `git revert` of the bad commit that flows through CI again. Practise it once before you need it at 3 a.m. The rule of thumb is to **roll back first and debug second**: get users working again, then investigate calmly with the logs.

## A release policy in code

Teams write down simple rules for when a deploy happens. For example:

- Only commits on `main` are deployed; feature branches are checked but never deployed.
- If any CI stage failed, the deploy is **blocked**.
- If everything passed on `main`, **deploy**.

These rules are logic like any other, which means you can write them as a function and test them. That's the second practice exercise.

## Containers in a nutshell

A virtual environment isolates your **Python packages**. It doesn't capture the Python interpreter itself, the operating system, or system libraries your packages might need. **Docker** goes further: a **container image** bundles the OS files, the Python interpreter, your dependencies and your code into one package that runs the same way anywhere Docker runs.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Read it top to bottom: start from an official image that already has Python 3.12 on a small Linux, install the dependencies, copy your code in, and say what command to run. `docker build -t habit-api .` makes the image; `docker run -p 8000:8000 habit-api` starts a container from it.

```
venv:       your packages                            (uses the machine's Python and OS)
container:  your packages + Python + OS libraries    (runs the same on any Docker host)
```

You don't need Docker for your first deploys; a PaaS can build your app directly. But you'll see Dockerfiles in almost every company repository, so be able to read one.

## Common mistakes

**`ModuleNotFoundError` in CI or production but not locally.** You installed a package by hand and never added it to `pyproject.toml` (or `requirements.txt`). Add it, commit, and push. Testing in CI on a clean machine is exactly what catches this.

**The app starts locally but the deploy times out.** Usually the server is listening on `127.0.0.1` or a hard-coded port instead of `0.0.0.0` and `$PORT`. Check the start command.

**Committing the `.venv` folder.** It's large, specific to your machine, and useless elsewhere. Add `.venv/` to `.gitignore`; the lockfile is what you share.

**Unpinned or missing `requires-python`.** Without it, someone on Python 3.9 installs your project and gets baffling errors. State the versions you actually test.

**Deploying from a laptop.** "I'll just push it from my machine" skips the checks. Let the pipeline deploy, so every release has passed lint and tests.

> **Try it:** In the practice editor, paste the `pyproject.toml` from the top of this lesson into a triple-quoted string, load it with `tomllib.loads`, and print the dev dependency group. Then delete the closing `]` of the list and read the `TOMLDecodeError` message: it tells you the line and column.

## Recap

- `pyproject.toml` describes the project: name, supported Python, runtime dependencies and dev groups. A committed lockfile pins exact versions.
- `pip` + `venv` is the classic way; `uv` does the same faster and manages the lockfile for you.
- CI runs install → lint → test → build → deploy, cheapest first, and stops on the first non-zero exit code.
- Dev, staging and production run the same code with different config.
- A PaaS deploys from your repo; listen on `0.0.0.0` and `$PORT`, and set secrets in its dashboard.
- Health checks stop bad versions from going live; rollbacks undo the ones that slip through. Roll back first, debug second.
- A container bundles the OS, Python and your code; a venv only isolates packages.
