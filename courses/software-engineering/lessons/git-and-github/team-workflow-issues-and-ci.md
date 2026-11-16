# Team workflow, issues and CI

You now know the pieces: commits, branches, remotes and pull requests. This lesson puts them together into the workflow that most software teams follow every day. Work starts as an **issue**, happens on a **feature branch**, arrives as a **pull request**, gets checked automatically by **continuous integration**, and only then reaches a protected `main`. When you join a team, this loop is what "doing your job" looks like hour to hour, and showing it in your own projects tells employers you already know it.

## The feature-branch workflow

The rule at the centre is simple: **`main` always works, and nobody commits to it directly.** All changes go through branches and pull requests.

```
issue #42  ->  branch  ->  commits  ->  pull request  ->  CI + review  ->  merge to main
"Reset        fix-42-      small,       "Closes #42"      tests pass,      branch deleted,
 password"    reset-email  focused                        1 approval       issue closed
```

Step by step:

1. **Pick an issue** (or create one) and assign it to yourself, so nobody else starts the same work.
2. **Update `main` and branch from it:** `git switch main`, `git pull`, `git switch -c fix-42-reset-email`. Many teams put the issue number in the branch name.
3. **Work in small commits** on the branch. Push it early (`git push -u origin fix-42-reset-email`), so your work is backed up.
4. **Open a pull request** when it's ready, or a **draft PR** earlier if you want feedback on the approach. Link the issue with `Closes #42` in the description.
5. **CI runs, and teammates review.** Fix what they find by pushing more commits to the same branch.
6. **Merge** once the checks are green and the review is approved. Delete the branch. GitHub closes the issue automatically.

Because every change is a small, reviewed, tested branch, `main` stays deployable, and when something does break it's easy to find which PR did it.

## Issues: the unit of work

An **issue** is a tracked item of work: a bug, a feature, a question, a chore. GitHub Issues, Jira and Linear all work the same way. Each issue has a number (`#42`), a title, a description, comments, and usually labels (`bug`, `enhancement`, `good first issue`) and an assignee.

A good issue lets someone who wasn't in the conversation pick it up:

```markdown
**Title:** Password reset email is never sent

**What happens:** Submitting the "Forgot password" form shows "Email sent",
but no email arrives (checked spam). Started after Tuesday's deploy.

**Expected:** An email with a reset link arrives within a minute.

**Steps to reproduce:**
1. Go to /forgot-password
2. Enter a registered email, submit

**Notes:** Logs show `SMTPAuthenticationError` at the time of each request.
```

That's the bug report structure from "Debugging systematically": what happened, what you expected, how to reproduce it, and evidence. Feature issues instead describe the problem a user has and what "done" looks like.

Issues and PRs link to each other by number. Writing `#42` anywhere on GitHub creates a link. In a PR description, `Closes #42`, `Fixes #42` or `Resolves #42` also closes the issue when the PR is merged into the default branch. That link is how, months later, someone reading a line of code can trace it back to the reason it exists.

## Protecting main

Rules are easier to follow when the tools enforce them. On GitHub, **branch protection rules** (or the newer **rulesets**, under the repository's Settings) can require, for `main`:

- **Changes only through pull requests**: direct pushes are refused.
- **At least one approving review** before merging.
- **Required status checks**: named CI checks must pass before the Merge button works.
- **No force pushes and no deletion** of the branch.

A **required check** is a CI job the branch rule names. If it fails, or hasn't finished, GitHub won't let the PR merge, not even for the person who wrote it. That turns "please run the tests before merging" from a polite request into a guarantee.

## Continuous integration

**Continuous integration (CI)** means every change is automatically built and tested on a clean machine, as soon as it's pushed, before it joins `main`. "Works on my machine" stops being an argument: the CI machine has none of your local settings or leftover files, so it catches the missing dependency in `requirements.txt` or the test that only passed because of a file you forgot to commit.

**GitHub Actions** is GitHub's built-in CI. You describe what to run in a **workflow file**, a YAML file in your repository under `.github/workflows/`. (YAML is a configuration format where indentation shows structure, like Python.)

Here's a complete workflow that runs a Python project's tests:

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

Reading it from the top:

- **`name`**: what GitHub shows in the Actions tab and on the PR.
- **`on`**: the **triggers**. This workflow runs on every push to `main` and on every pull request (when it's opened, and every time new commits are pushed to it).
- **`jobs`**: one or more **jobs**. Each job runs on a fresh virtual machine (`runs-on: ubuntu-latest`). Separate jobs run in parallel.
- **`strategy.matrix`**: run the same job once per value, here once for Python 3.12 and once for 3.13. They show up as two checks, `test (3.12)` and `test (3.13)`.
- **`steps`**: what the job does, in order. A step either **`uses`** a ready-made action (`actions/checkout` downloads your repository's code onto the machine; `actions/setup-python` installs Python) or **`run`s** shell commands, exactly as you'd type them in a terminal.

Each command's **exit code** decides the result. A program that finishes normally exits with `0`; a non-zero exit means failure. `pytest` exits with `1` if any test fails. **If any step exits non-zero, the step fails, the remaining steps are skipped, and the job is marked as failed.** That's the whole mechanism: CI is just "run commands, check exit codes". You'll write a small version of this rule in the practice.

Commit the file, push, and open the **Actions** tab on GitHub to watch it run. On a PR, the result appears near the Merge button as a green tick, a red cross, or a yellow dot while it's running.

> **Note:** a project with tests and green CI on GitHub is one of the clearest signals you can give an employer. Every project you build from the testing section onward should have it.

## Reading a red CI run

A red cross on your PR isn't a judgement, it's information. Read it the way you read a traceback:

1. **Click "Details"** next to the failed check. You'll see the job's steps; the failed one is marked and expanded.
2. **Scroll to the end of the failed step's log.** As with tracebacks, the useful part is at the bottom. For pytest, look for the `FAILED` lines and the short summary:

```
FAILED tests/test_cart.py::test_empty_cart_total - ZeroDivisionError: division by zero
========================= 1 failed, 23 passed in 0.41s =========================
Error: Process completed with exit code 1.
```

3. **Work out which kind of failure it is:**
   - **A test failed:** your change broke behaviour, or the test needs updating because the behaviour changed on purpose. Reproduce it locally by running that one test: `pytest tests/test_cart.py::test_empty_cart_total`.
   - **The job errored before the tests:** for example `ModuleNotFoundError` during install. Often a dependency missing from `requirements.txt`: it was installed on your machine but you never recorded it. Exactly the kind of bug CI exists to catch.
   - **It fails in only one matrix job:** a version difference, say a feature that exists in Python 3.13 but not in 3.12.
4. **Fix it on your branch, push, and CI runs again** automatically.

If a test fails on CI sometimes and passes on re-run, it's **flaky**, usually because it depends on time, randomness, ordering or the network. Don't just re-run until it's green; flaky tests teach a team to ignore red, which is worse than no tests. (You'll learn to avoid them in the testing section by injecting things like `now` and `rng`, as several exercises in this course already do.)

## Common mistakes

**Pushing straight to `main`.** On a protected repository it's refused; on an unprotected one it skips review and CI. Always branch.

**Opening a PR without running the tests locally.** CI will tell you, but ten minutes later and in public. Run `pytest` before you push.

**A workflow file in the wrong place.** It must be in `.github/workflows/` (note the dot and the plural) and end in `.yml` or `.yaml`, or GitHub ignores it silently.

**YAML indentation errors.** Like Python, indentation is structure, but YAML doesn't allow tabs. GitHub shows "Invalid workflow file" with the line number.

**Forgetting to link the issue.** The work gets merged and the issue stays open for months. Put `Closes #N` in every PR description.

**Disabling a failing check to merge.** If a required check is wrong, fix the check in its own PR. Turning it off "just this once" is how broken code reaches production.

## Recap

- **Feature-branch workflow:** issue → branch from an up-to-date `main` → small commits → pull request with `Closes #N` → CI and review → merge → delete the branch.
- **Issues** are the unit of work. Write them so someone else can pick them up: what happens, what's expected, steps, evidence.
- **Protect `main`:** require PRs, reviews and passing **required checks**; block force pushes.
- **CI** runs your tests on a clean machine for every push and PR. A GitHub Actions workflow lives in `.github/workflows/`, has triggers (`on`), jobs (each on a fresh machine) and steps (`uses` or `run`). Any non-zero exit code fails the job.
- To read a red run, open the failed step, read the end of the log, decide whether a test failed or the job errored, and reproduce it locally.
