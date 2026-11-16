import ast


def call_graph(source: str) -> dict[str, set[str]]:
    """Map each top-level function to the module's functions it calls by name."""
    tree = ast.parse(source)
    # TODO: collect the top-level FunctionDef / AsyncFunctionDef nodes from tree.body
    # TODO: for each one, walk it and collect ast.Call nodes whose .func is an ast.Name
    # TODO: keep only names that are top-level functions in this module
    return {}


if __name__ == "__main__":
    source = '''
def load(path):
    return open(path).read()

def parse(text):
    return [line.split(",") for line in text.splitlines()]

def main(path):
    rows = parse(load(path))
    print(len(rows))
'''
    print(call_graph(source))
