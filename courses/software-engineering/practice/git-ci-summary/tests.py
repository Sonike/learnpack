from solution import ci_exit_code, ci_summary


def job(name, *outcomes, status="ok"):
    tests = [{"name": f"test_{i}", "outcome": o} for i, o in enumerate(outcomes, start=1)]
    return {"job": name, "status": status, "tests": tests}


def test_all_green_run_passes():
    results = [job("test (3.12)", "passed", "passed"), job("test (3.13)", "passed", "skipped")]
    assert ci_exit_code(results) == 0, "nothing failed, so the exit code should be 0"
    got = ci_summary(results)
    want = "## CI passed\n**3 passed, 0 failed, 1 skipped** across 2 jobs"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_a_failed_test_fails_the_run_and_is_listed():
    results = [job("test (3.12)", "passed", "failed", "skipped")]
    assert ci_exit_code(results) == 1, "a failed test should give exit code 1"
    got = ci_summary(results)
    want = (
        "## CI failed\n**1 passed, 1 failed, 1 skipped** across 1 job\n\n"
        "### Problems\n- `test (3.12)`: `test_2` failed"
    )
    assert got == want, f"expected {want!r}, got {got!r}"


def test_an_errored_job_fails_the_run_even_with_no_failed_tests():
    results = [job("test (3.12)", "passed"), job("lint", status="error")]
    assert ci_exit_code(results) == 1, "a job that errored must fail the run"
    got = ci_summary(results)
    want = (
        "## CI failed\n**1 passed, 0 failed, 0 skipped** across 2 jobs\n\n"
        "### Problems\n- `lint`: job errored"
    )
    assert got == want, f"expected {want!r}, got {got!r}"


def test_problems_are_listed_job_by_job():
    results = [job("a", "failed", "passed", "failed"), job("b", "failed", status="error")]
    got = ci_summary(results).split("### Problems\n")[1]
    want = "- `a`: `test_1` failed\n- `a`: `test_3` failed\n- `b`: job errored\n- `b`: `test_1` failed"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_skipped_tests_do_not_fail_the_run():
    results = [job("test (3.12)", "skipped", "skipped")]
    assert ci_exit_code(results) == 0, "skipped tests should not fail the run"
    assert ci_summary(results).startswith("## CI passed"), "the heading should say passed"
