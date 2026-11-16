import ast


def call_graph(source: str) -> dict[str, set[str]]:
    """Map each top-level function to the module's functions it calls by name."""
    tree = ast.parse(source)
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    names = {f.name for f in functions}
    graph = {}
    for func in functions:
        calls = set()
        for node in ast.walk(func):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in names:
                calls.add(node.func.id)
        graph[func.name] = calls
    return graph
