# Guard against hallucinated packages

AI assistants sometimes import packages that **don't exist**, or that exist under a different name. Attackers know this: they register those made-up names on PyPI with malicious code inside, waiting for someone to `pip install` them. Before installing anything an assistant suggests, check it.

Write `check_imports(code: str, known_packages: set[str]) -> list[str]`.

- `code` is Python source code as a string.
- `known_packages` is the set of top-level module names your team has approved (for example `{"fastapi", "pydantic"}`).
- Return a **sorted list without duplicates** of every imported top-level module name that is **neither** in the standard library **nor** in `known_packages`.

Details:
- Use `ast.parse` and walk the tree; don't search the text with string methods (an `import` inside a string or comment isn't a real import).
- `import a.b.c` and `from a.b import c` both import the top-level module `a`.
- Ignore relative imports such as `from . import utils` or `from .models import User` (they're your own project's files).
- `sys.stdlib_module_names` is a set of every standard-library module name.

## Example

```python
code = """
import os, json
import requestz
from fastapi import FastAPI
from sklearn.model_selection import train_test_split
from . import helpers
"""
check_imports(code, {"fastapi"})
# ['requestz', 'sklearn']
```

> **Note:** a module name isn't always the package name you install. `import bs4` comes from the package `beautifulsoup4`, and `import sklearn` from `scikit-learn`. Your function only checks module names; a human still looks up the package on pypi.org before installing.
