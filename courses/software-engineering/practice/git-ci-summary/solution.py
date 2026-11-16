def problems(results: list[dict]) -> list[str]:
    """One Markdown bullet per errored job or failed test, job by job."""
    bullets = []
    for job in results:
        if job["status"] == "error":
            bullets.append(f"- `{job['job']}`: job errored")
        for test in job["tests"]:
            if test["outcome"] == "failed":
                bullets.append(f"- `{job['job']}`: `{test['name']}` failed")
    return bullets


def ci_exit_code(results: list[dict]) -> int:
    """1 if any test failed or any job errored, else 0."""
    return 1 if problems(results) else 0


def ci_summary(results: list[dict]) -> str:
    """A Markdown PR comment summarising the run."""
    counts = {"passed": 0, "failed": 0, "skipped": 0}
    for job in results:
        for test in job["tests"]:
            counts[test["outcome"]] += 1

    jobs = "job" if len(results) == 1 else "jobs"
    bullets = problems(results)
    lines = [
        "## CI failed" if bullets else "## CI passed",
        f"**{counts['passed']} passed, {counts['failed']} failed, {counts['skipped']} skipped**"
        f" across {len(results)} {jobs}",
    ]
    if bullets:
        lines += ["", "### Problems", *bullets]
    return "\n".join(lines)
