def ci_exit_code(results: list[dict]) -> int:
    """1 if any test failed or any job errored, else 0."""
    # TODO
    return 0


def ci_summary(results: list[dict]) -> str:
    """A Markdown PR comment summarising the run."""
    lines = []
    # TODO: heading "## CI passed" / "## CI failed"
    # TODO: totals line "**P passed, F failed, S skipped** across N jobs" ("1 job" when N == 1)
    # TODO: if there are problems: "", "### Problems", then the bullets
    return "\n".join(lines)


if __name__ == "__main__":
    results = [
        {"job": "test (3.12)", "status": "ok", "tests": [
            {"name": "test_login", "outcome": "passed"},
            {"name": "test_logout", "outcome": "failed"},
            {"name": "test_slow_export", "outcome": "skipped"},
        ]},
        {"job": "lint", "status": "error", "tests": []},
    ]
    print("exit code:", ci_exit_code(results))
    print(ci_summary(results))
