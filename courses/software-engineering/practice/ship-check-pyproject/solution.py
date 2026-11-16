import re
import tomllib

VERSION_CHARS = "<>=!~"


def requirement_name(requirement: str) -> str:
    """'pytest>=8' -> 'pytest'. Lower-cased name before any version marker."""
    return re.split(r"[<>=!~;\[ ]", requirement.strip(), maxsplit=1)[0].lower()


def has_test_dependency(data: dict) -> bool:
    groups = dict(data.get("dependency-groups", {}))
    groups.update(data["project"].get("optional-dependencies", {}))
    for requirements in groups.values():
        for requirement in requirements:
            if isinstance(requirement, str) and requirement_name(requirement) == "pytest":
                return True
    return False


def check_pyproject(text: str) -> list[str]:
    """Return a list of problems found in a pyproject.toml file."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return ["invalid TOML"]
    if "project" not in data:
        return ["missing [project] table"]

    project = data["project"]
    problems = []
    if "requires-python" not in project:
        problems.append("missing requires-python")
    for requirement in project.get("dependencies", []):
        if not any(char in requirement for char in VERSION_CHARS):
            problems.append(f"unpinned dependency: {requirement.strip()}")
    if not has_test_dependency(data):
        problems.append("missing test dependency (pytest)")
    return problems
