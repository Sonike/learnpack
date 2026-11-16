# Type hints

## Why this matters

`def total(items, discount)`: is `items` a list of prices, a list of dicts, or a dict? Is `discount` a percentage, a fraction or an amount in cents? Without help, the only way to know is to read the whole function, or run it and see what breaks. **Type hints** write the answer into the code. Editors use them to autocomplete and to underline mistakes as you type, teammates read them as documentation, AI assistants use them to make better suggestions, and a **type checker** can find whole classes of bugs before you run anything. Almost every professional Python codebase uses them now.

## Annotating functions

A type hint (also called an **annotation**) goes after a parameter name with a colon, and after the parameter list with an arrow for the return value:

```python
def greet(name: str, times: int) -> str:
    return ("Hello, " + name + "! ") * times


print(greet("Ada", 2))   # Hello, Ada! Hello, Ada!
```

Read it as "`greet` takes a `str` and an `int` and returns a `str`". A function that returns nothing is annotated `-> None`:

```python
def log(message: str) -> None:
    print(message)
```

You can annotate variables too, though you rarely need to, because tools work out most variable types from the value:

```python
count: int = 0
names: list[str] = []      # useful: an empty list says nothing about what goes in it
```

## Hints aren't checked when the program runs

This surprises everyone at first. Python **ignores** type hints at runtime:

```python
def double(n: int) -> int:
    return n * 2


print(double("ha"))   # haha   no error!
```

The hint says `int`, we passed a `str`, and Python ran it anyway, because `"ha" * 2` is valid Python. Hints are information for tools and people, not rules Python enforces. The tool that enforces them is a **type checker**, which you run separately (more on that below). If you need a check at runtime, for example on user input, write it yourself with `if` and `raise`.

## Collection types

Inside square brackets you say what a collection holds:

```python
def average(scores: list[float]) -> float:
    return sum(scores) / len(scores)


def word_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def first_and_last(names: list[str]) -> tuple[str, str]:
    return names[0], names[-1]


print(word_counts("a b a"))   # {'a': 2, 'b': 1}
```

- `list[float]`: a list of floats.
- `dict[str, int]`: a dict with `str` keys and `int` values.
- `tuple[str, str]`: a tuple of exactly two strings. (`tuple[int, ...]` means "any number of ints".)
- `set[str]`: a set of strings.

These lowercase forms work from Python 3.9 on. In older code you'll see `List[float]` and `Dict[str, int]` imported from `typing`; they mean the same thing.

## "Or": `X | None` and unions

Many functions sometimes return a value and sometimes don't. `dict.get` is the classic: it returns `None` when the key is missing.

```python
def find_age(ages: dict[str, int], name: str) -> int | None:
    return ages.get(name)


print(find_age({"Ada": 36}, "Ada"))     # 36
print(find_age({"Ada": 36}, "Grace"))   # None
```

`int | None` means "an `int` or `None`". The `|` reads as "or" and works for any types: `int | str`, `str | list[str]`. In older code you'll see the same thing written `Optional[int]` (from `typing`), which means exactly `int | None`. It doesn't mean "an optional argument"; it means "might be `None`".

This is where hints start catching real bugs. Look:

```python
def total_age(ages: dict[str, int], names: list[str]) -> int:
    total = 0
    for name in names:
        total += find_age(ages, name)
    return total


total_age({"Ada": 36}, ["Ada", "Grace"])
# TypeError: unsupported operand type(s) for +=: 'int' and 'NoneType'
```

Without hints you find this bug when it crashes. With hints, a type checker reports it before you run anything, because `find_age` is declared to return `int | None` and you're adding it to an `int` without checking. The fix is to handle `None`:

```python
    for name in names:
        age = find_age(ages, name)
        if age is not None:
            total += age
```

After the `if age is not None:` check, the type checker knows `age` is an `int`. This is called **narrowing**.

## Functions as values: `Callable`

When a parameter is itself a function, annotate it with `Callable[[argument types], return type]`:

```python
from collections.abc import Callable


def apply_all(values: list[int], fn: Callable[[int], int]) -> list[int]:
    return [fn(v) for v in values]


print(apply_all([1, 2, 3], lambda n: n * 10))   # [10, 20, 30]
```

`Callable[[int], int]` reads "a function that takes one `int` and returns an `int`". `Callable` also exists in `typing`; importing it from `collections.abc` is the modern recommendation.

## Hints on classes

Methods are annotated like functions (`self` doesn't need a hint), and dataclass fields need hints anyway:

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    email: str
    phone: str | None = None

    def contact(self) -> str:
        return self.phone or self.email


def find_user(users: list[User], name: str) -> User | None:
    for user in users:
        if user.name == name:
            return user
    return None
```

Your own classes are types too: `list[User]`, `User | None`.

## Running a type checker

A type checker reads your code without running it and reports places where the types don't line up. The two common ones are **mypy** and **pyright** (pyright is what powers Pylance, the Python extension in VS Code, so you may already see its squiggly underlines). Install one in your project's virtual environment and run it on a file:

```bash
pip install mypy
mypy ages.py
```

For the buggy `total_age` above, mypy prints something like:

```
ages.py:9: error: Unsupported operand types for + ("int" and "None")  [operator]
ages.py:9: note: Right operand is of type "int | None"
Found 1 error in 1 file (checked 1 source file)
```

Read it like any error: file, line, then what's wrong. It found the bug without running a single line. Pyright works the same way (`pip install pyright`, then `pyright ages.py`). Teams usually run one of them in CI (automatic checks on every pull request), next to the tests and the linter.

> **Note:** you can read the hints of a function from code with `typing.get_type_hints(fn)`. Some tools, like FastAPI and dataclasses, use hints at runtime to do real work, which is part of why they're everywhere now.

## How much to annotate

A sensible rule for beginners and teams alike:

- Annotate every function's parameters and return type. That's where hints help most: at the boundaries between pieces of code.
- Don't annotate local variables unless the tool can't work it out (like an empty list or dict).
- Avoid `Any` (from `typing`, meaning "anything goes"). It switches checking off. Sometimes it's the honest answer for messy JSON, but use it on purpose, not as an escape hatch.

> **Note:** AI coding assistants use your hints as context. A function signed `def parse(rows: list[dict[str, str]]) -> list[Order]` gets far better suggestions and explanations than `def parse(rows)`. The same goes for the human reading your pull request.

## Common mistakes

**Expecting Python to enforce hints.** It won't. `double("ha")` runs. Run a type checker, or validate input yourself.

**Forgetting `None` in the return type.** If any path returns `None` (including falling off the end of the function), the return type must say `| None`. Type checkers report this as `Missing return statement` or `Incompatible return value type (got "None", expected "int")`.

**Using a value that might be `None` without checking.** The most common error a checker finds. The fix is almost always an `if x is None:` branch.

**`list` vs `list[int]`.** Plain `list` says "a list of anything". Be specific; that's where the value is.

**Writing `list[int]` on very old Python.** Before 3.9 it raised `TypeError: 'type' object is not subscriptable`. You won't hit this on 3.12, but you'll see `List[int]` from `typing` in older code and answers online.

**Strings in a numeric context.** `"Ada is " + 36` fails with `TypeError: can only concatenate str (not "int") to str`. A checker catches it from the hints; the clean fix is an f-string, `f"Ada is {age}"`.

## Recap

- Hints describe what functions take and return: `def f(names: list[str], limit: int | None = None) -> dict[str, int]:`.
- Python ignores them at runtime. Type checkers (mypy, pyright) read them and find bugs before you run the code.
- `X | None` (old spelling: `Optional[X]`) means "might be `None`"; check before using it.
- `Callable[[int], int]` describes a function parameter.
- Annotate every function boundary; let tools work out the rest.
