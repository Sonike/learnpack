# Map who calls whom

When you join a team, one of the fastest ways to understand a module is to see which functions call which. Editors do this with "Find all references" and "Go to definition". You'll build a tiny version with Python's `ast` module, which turns source code into a tree of objects you can inspect.

Write `call_graph(source: str) -> dict[str, set[str]]`.

- `source` is the text of a Python module.
- The result has one key per **top-level function** in the module (`def` or `async def` at the outermost level, not methods inside classes).
- Each value is the set of **those same top-level functions** that the function calls **by plain name**, like `load()`. Calls to anything else (`print()`, `len()`, imported functions, `obj.method()`) are left out.
- A function that calls nothing from the module maps to an empty `set()`. A recursive function includes its own name.

## Example

```python
source = '''
def load(path):
    return open(path).read()

def parse(text):
    return [line.split(",") for line in text.splitlines()]

def main(path):
    rows = parse(load(path))
    print(len(rows))
'''
call_graph(source)
# {'load': set(), 'parse': set(), 'main': {'load', 'parse'}}
```

> **Hint:** `tree = ast.parse(source)`; `tree.body` is the list of top-level statements. For each function node, `ast.walk(node)` visits everything inside it. A call to a plain name is an `ast.Call` whose `.func` is an `ast.Name`; the name is `.func.id`.

> **Try it:** `print(ast.dump(ast.parse("main(x)"), indent=2))` shows you the tree for one call.
