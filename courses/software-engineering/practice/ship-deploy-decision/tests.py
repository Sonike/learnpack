from solution import deploy_decision


def test_deploys_main_when_lint_and_test_pass():
    got = deploy_decision({"lint": "passed", "test": "passed", "docs": "skipped"}, "main")
    want = "deploy"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_blocks_main_when_a_required_stage_fails():
    got = [deploy_decision({"lint": "failed", "test": "passed"}, "main"),
           deploy_decision({"lint": "passed", "test": "failed"}, "main")]
    want = ["block", "block"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_blocks_when_a_required_stage_is_missing_or_skipped():
    got = [deploy_decision({"lint": "passed"}, "main"),
           deploy_decision({"lint": "passed", "test": "skipped"}, "main"),
           deploy_decision({}, "main")]
    want = ["block", "block", "block"]
    assert got == want, f"expected {want!r}, got {got!r}"


def test_blocks_when_any_other_stage_fails():
    got = deploy_decision({"lint": "passed", "test": "passed", "build": "failed"}, "main")
    want = "block"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_skips_every_branch_except_main():
    got = [deploy_decision({"lint": "passed", "test": "passed"}, "feature/login"),
           deploy_decision({"lint": "failed"}, "Main")]
    want = ["skip", "skip"]
    assert got == want, f"expected {want!r}, got {got!r}"
