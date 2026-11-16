from solution import call_graph

SOURCE = '''
import json

def load(path):
    return open(path).read()

def parse(text):
    return json.loads(text)

def main(path):
    data = parse(load(path))
    print(len(data))
'''


def test_finds_calls_between_module_functions():
    got = call_graph(SOURCE)
    want = {"load": set(), "parse": set(), "main": {"load", "parse"}}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_ignores_builtins_and_attribute_calls():
    got = call_graph("def f(items):\n    items.sort()\n    return len(items)\n")
    assert got == {"f": set()}, f"expected {{'f': set()}}, got {got!r}"


def test_recursive_function_calls_itself():
    got = call_graph("def fact(n):\n    return 1 if n < 2 else n * fact(n - 1)\n")
    assert got == {"fact": {"fact"}}, f"expected {{'fact': {{'fact'}}}}, got {got!r}"


def test_includes_async_functions():
    src = "async def fetch():\n    return 1\n\nasync def run():\n    return await fetch()\n"
    got = call_graph(src)
    want = {"fetch": set(), "run": {"fetch"}}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_skips_methods_inside_classes():
    src = "def helper():\n    pass\n\nclass Box:\n    def open(self):\n        helper()\n"
    got = call_graph(src)
    assert got == {"helper": set()}, f"expected {{'helper': set()}}, got {got!r}"


def test_empty_module_gives_empty_graph():
    got = call_graph("")
    assert got == {}, f"expected {{}}, got {got!r}"
