REQUIRED = ("lint", "test")


def deploy_decision(ci_results: dict[str, str], branch: str) -> str:
    """Return "deploy", "block" or "skip" for this commit."""
    # TODO: not main -> "skip"
    # TODO: a required stage missing or not "passed" -> "block"
    # TODO: any stage "failed" -> "block"
    return "skip"


if __name__ == "__main__":
    print(deploy_decision({"lint": "passed", "test": "passed"}, "main"))        # deploy
    print(deploy_decision({"lint": "passed", "test": "failed"}, "main"))        # block
    print(deploy_decision({"lint": "passed", "test": "passed"}, "feature/x"))   # skip
