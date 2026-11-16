REQUIRED = ("lint", "test")


def deploy_decision(ci_results: dict[str, str], branch: str) -> str:
    """Return "deploy", "block" or "skip" for this commit."""
    if branch != "main":
        return "skip"
    if any(ci_results.get(stage) != "passed" for stage in REQUIRED):
        return "block"
    if "failed" in ci_results.values():
        return "block"
    return "deploy"
