import re
import tomllib


def requirement_name(requirement: str) -> str:
    """'pytest>=8' -> 'pytest'. Lower-cased name before any version marker."""
    # TODO: re.split on the marker characters and take the first part
    return requirement


def check_pyproject(text: str) -> list[str]:
    """Return a list of problems found in a pyproject.toml file."""
    problems = []
    # TODO: parse with tomllib.loads; on TOMLDecodeError return ["invalid TOML"]
    # TODO: no "project" table -> return ["missing [project] table"]
    # TODO: check requires-python, unpinned dependencies, and a pytest test dependency
    return problems


if __name__ == "__main__":
    sample = '''
[project]
name = "habit-api"
dependencies = ["fastapi>=0.115", "requests"]

[dependency-groups]
dev = ["ruff>=0.6"]
'''
    for problem in check_pyproject(sample):
        print("-", problem)
