# Should we deploy?

Teams write down a **release policy**: the rules that decide whether a change goes to production. Write it as a function, so it can be tested like any other logic.

```python
def deploy_decision(ci_results: dict[str, str], branch: str) -> str:
```

- `ci_results`: the result of each CI stage, for example `{"lint": "passed", "test": "failed"}`. Each value is `"passed"`, `"failed"` or `"skipped"`.
- `branch`: the Git branch the commit is on, such as `"main"` or `"feature/login"`.
- Return exactly one of `"deploy"`, `"block"` or `"skip"`.

## The policy

1. Only `main` is ever deployed. On any other branch, return `"skip"`.
2. On `main`, the required stages `"lint"` and `"test"` must both be present and `"passed"`. If either is missing or not `"passed"`, return `"block"`.
3. On `main`, if any other stage is `"failed"`, return `"block"`. (Other stages may be `"skipped"`.)
4. Otherwise return `"deploy"`.

## Examples

```python
deploy_decision({"lint": "passed", "test": "passed"}, "main")              # 'deploy'
deploy_decision({"lint": "passed", "test": "failed"}, "main")              # 'block'
deploy_decision({"lint": "passed", "test": "passed"}, "feature/login")     # 'skip'
deploy_decision({"lint": "passed"}, "main")                                # 'block' (no test result)
deploy_decision({"lint": "passed", "test": "passed", "docs": "skipped"}, "main")  # 'deploy'
```
