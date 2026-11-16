# Ship it: deploy your API

Take the REST API you built in the web section and turn it into a running service that a stranger can use, that you can debug from its logs, and that you can roll back in a minute. Recruiters and interviewers click links. A live URL with a green CI badge and a design doc says "this person can ship" more clearly than any line on a resume.

## What you'll build

Work in the same GitHub repository as your API (or a fork of it). By the end you'll have:

1. **Configuration from the environment.** A `load_config(env)` function like the one from Configuration and secrets, returning a `Config` dataclass. The app calls it once at startup and refuses to start, with a clear message, if a required setting is missing. Commit a `.env.example`; git-ignore `.env`.
2. **No secrets in the repo.** Add your `find_secrets` check as a script (and, if you like, a pre-commit hook), and run it in CI. If you ever committed a real key, rotate it and note it in the PR.
3. **Structured logging.** Your `JsonFormatter` on the root logger, with your `redact` step applied to anything request-shaped. Log one line per request with method, path, status, duration in milliseconds and a request ID. Return the request ID in an `X-Request-ID` response header.
4. **A CI pipeline.** GitHub Actions: install → `ruff check` → `pytest` → deploy, where the deploy step runs only on `main` and only if everything before it passed.
5. **A live deploy** on a free platform (Render or PythonAnywhere work well), with a `GET /health` endpoint the platform uses as its health check, and secrets set in the platform's dashboard.
6. **A one-page design doc** (`docs/design.md`): problem, components (draw the ASCII diagram), data model, and at least one trade-off you made and why (for example SQLite vs Postgres, or what you chose not to build).
7. **A tested rollback.** Deploy a deliberately broken change (say, `/health` returns 500), watch the platform refuse it or roll it back yourself, and write down the steps and how long it took.

## Suggested order

```
Day 1  Config: load_config + .env.example + startup failure test
Day 2  Logging: JsonFormatter, redaction, request-ID middleware
Day 3  CI: ruff + pytest on every push; branch protection on main
Day 4  Deploy: platform setup, env vars, /health, deploy from CI
Day 5  Design doc + rollback drill + README polish
```

## README must include

- The live URL and a one-line description at the very top.
- A CI badge.
- How to run locally (`cp .env.example .env`, install, run, test).
- A table of every environment variable: name, required or not, default, what it does.
- A sample log line, so readers can see what the logs look like.
- A link to the design doc and a short note on the rollback drill.

## How it's judged

| Area | Looks good when… |
|---|---|
| Config | A missing setting stops startup with a message naming it; tests cover parsing |
| Secrets | `git log -p` shows no keys; the scan runs in CI |
| Logs | One JSON object per line; a request ID ties lines together; no passwords or tokens anywhere |
| CI/CD | Lint and tests gate every PR; only `main` deploys |
| Deploy | The URL works; `/health` returns 200; secrets live only in the platform |
| Design | The doc names a real trade-off, not just a list of tools |
| Rollback | The steps are written down and were actually tried |

> **Note:** free hosting tiers often put apps to sleep after a period with no traffic, so the first request can take 30 seconds or more. Mention it in your README so a reviewer doesn't think the app is broken.
