import ast
import sys


def check_imports(code: str, known_packages: set[str]) -> list[str]:
    """Return sorted top-level imports that are neither stdlib nor approved."""
    tree = ast.parse(code)
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.add(node.module.split(".")[0])
    allowed = sys.stdlib_module_names | set(known_packages)
    return sorted(name for name in found if name not in allowed)
