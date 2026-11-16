# Summarise a CI run for a pull request

**Continuous integration** (CI) runs your tests on every pull request, often in several **jobs** (for example one per Python version, plus a linting job). Many teams have a bot post a short summary as a PR comment. Write the two functions behind such a bot.

```python
def ci_exit_code(results: list[dict]) -> int:
def ci_summary(results: list[dict]) -> str:
```

`results` has one dict per job:

```python
{"job": "test (3.12)", "status": "ok", "tests": [{"name": "test_login", "outcome": "passed"}, ...]}
```

- `status` is `"ok"` if the job ran to the end, or `"error"` if it crashed before finishing (say `pip install` failed). An errored job may have run only some tests, or none.
- Each test's `outcome` is `"passed"`, `"failed"` or `"skipped"`.

**`ci_exit_code`** returns `1` (failure) if **any test failed or any job errored**, otherwise `0`. Skipped tests don't fail a run. Note the second half of the rule: a job that crashed before running any tests has zero failed tests, and must still fail the run.

**`ci_summary`** returns Markdown made of these lines, joined with `"\n"`:

1. `## CI passed` or `## CI failed` (failed exactly when `ci_exit_code` is 1).
2. `**P passed, F failed, S skipped** across N jobs` with the totals over all jobs (`1 job`, singular, when N is 1).
3. Only if there are problems: a blank line, `### Problems`, then one bullet per problem, job by job in order. For each job: first `` - `JOB`: job errored `` if its status is `"error"`, then `` - `JOB`: `TEST` failed `` for each failed test in order.

## Example

```python
results = [
    {"job": "test (3.12)", "status": "ok", "tests": [
        {"name": "test_login", "outcome": "passed"},
        {"name": "test_logout", "outcome": "failed"},
        {"name": "test_slow_export", "outcome": "skipped"},
    ]},
    {"job": "lint", "status": "error", "tests": []},
]
ci_exit_code(results)   # 1
print(ci_summary(results))
```

```
## CI failed
**1 passed, 1 failed, 1 skipped** across 2 jobs

### Problems
- `test (3.12)`: `test_logout` failed
- `lint`: job errored
```
