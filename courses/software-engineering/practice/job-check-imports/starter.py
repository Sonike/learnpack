import ast
import sys


def check_imports(code: str, known_packages: set[str]) -> list[str]:
    """Return sorted top-level imports that are neither stdlib nor approved."""
    tree = ast.parse(code)
    found = set()
    for node in ast.walk(tree):
        # TODO: handle ast.Import (node.names is a list; each has .name)
        # TODO: handle ast.ImportFrom (node.module, and node.level > 0 means relative)
        pass
    # TODO: keep only names not in sys.stdlib_module_names and not in known_packages
    return sorted(found)


if __name__ == "__main__":
    code = """
import os, json
import requestz
from fastapi import FastAPI
from sklearn.model_selection import train_test_split
from . import helpers
"""
    print(check_imports(code, {"fastapi"}))  # expected ['requestz', 'sklearn']
