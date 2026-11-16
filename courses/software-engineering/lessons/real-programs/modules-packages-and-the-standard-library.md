# Modules, packages and the standard library

Programs past a few hundred lines don't live in one file, and nobody writes everything from scratch. Engineers split their code into **modules**, and lean on the huge amount of code that already exists: Python's standard library, and hundreds of thousands of packages other people have published. Knowing what's already available, and how to read its documentation, saves you days of work.

## import and modules

A **module** is simply a `.py` file. Every file you write is already a module, and `import` lets one file use what another one defines.

Python comes with many modules built in. Here's `math`:

```python
import math

print(math.sqrt(16))   # 4.0
print(math.pi)         # 3.141592653589793
```

`import math` runs the module once and gives you a name, `math`, through which you reach everything inside it with a dot. There are a few other forms:

```python
from math import sqrt, pi        # bring specific names in directly
print(sqrt(16))                  # 4.0

import datetime as dt            # a shorter alias
print(dt.date(2026, 11, 13))     # 2026-11-13
```

Prefer `import module` or `from module import name`. Avoid `from module import *`: it dumps every name into your file, and readers can't tell where anything came from.

## Your own modules

Say you have two files in the same folder:

```python
# pricing.py
VAT_RATE = 0.2

def with_vat(price):
    return round(price * (1 + VAT_RATE), 2)
```

```python
# main.py
from pricing import with_vat

print(with_vat(10))   # 12.0
```

Run `python main.py` and Python finds `pricing.py` because it looks in the folder of the script you ran first, then in the standard library, then in installed packages. That search list is `sys.path` if you're curious.

> **Note:** never name your own file after a module you want to use. A file called `random.py` or `json.py` in your project folder gets imported *instead of* the real one, and you get baffling errors like `AttributeError: module 'random' has no attribute 'randint'`.

### Packages

A **package** is a folder of modules. You import from it with dots:

```
shop/
    __init__.py
    pricing.py
    stock.py
main.py
```

```python
from shop.pricing import with_vat
```

The `__init__.py` file (often empty) marks the folder as a regular package. "Package" also has a second meaning: something you install with `pip`, like `requests` or `fastapi`. Context usually makes it clear.

## if __name__ == "__main__":

Every module has a variable called `__name__`. When you **run** a file directly, Python sets it to the string `"__main__"`. When the file is **imported**, `__name__` is the module's name instead.

```python
# pricing.py
def with_vat(price):
    return round(price * 1.2, 2)

print("__name__ is", __name__)

if __name__ == "__main__":
    print(with_vat(10))
```

```bash
$ python pricing.py
__name__ is __main__
12.0
$ python -c "import pricing"
__name__ is pricing
```

So the code under `if __name__ == "__main__":` runs only when the file is the program you started, never when another file imports it. That's where you put a script's "start here" code: parsing command-line arguments, calling `main()`, quick demo calls. Without it, importing your module to reuse one function would also run the whole script. (The practice starters in this course use this pattern for the code you Run.)

## A tour of the standard library

Python's motto is "batteries included". The **standard library** is everything that ships with Python, no install needed. Before writing a utility yourself, check whether it's already there. These are the modules you'll use most.

**`random`**: random choices, for games, sampling and test data.

```python
import random

rng = random.Random(42)              # a seeded generator gives repeatable results
print(rng.randint(1, 6))             # a number from 1 to 6
print(rng.choice(["red", "green"]))  # one item from a list
```

Passing a seeded `Random` object into functions, instead of calling `random.randint` directly, makes code that depends on randomness testable.

**`datetime`**: dates, times and the differences between them.

```python
from datetime import date, timedelta

deadline = date.fromisoformat("2026-12-25")
today = date(2026, 11, 13)
print((deadline - today).days)          # 42
print(today + timedelta(weeks=2))       # 2026-11-27
print(today.strftime("%d %B %Y"))       # 13 November 2026
```

Subtracting two dates gives a `timedelta`; its `.days` is a whole number of days. `datetime` handles month lengths and leap years for you. In real code you'd use `date.today()`; in functions you want to test, take `today` as a parameter so the result doesn't change every day.

**`collections`**: extra data structures. `Counter` counts things, and `defaultdict` gives missing keys a starting value.

```python
from collections import Counter, defaultdict

words = "the cat and the hat and the bat".split()
counts = Counter(words)
print(counts["the"])            # 3
print(counts.most_common(2))    # [('the', 3), ('and', 2)]

by_letter = defaultdict(list)
for w in words:
    by_letter[w[0]].append(w)   # no need to check whether the key exists
print(by_letter["h"])           # ['hat']
```

**`itertools`**: tools for looping, such as `islice` (take the first n items of anything) and `chain` (loop over several lists as one).

**`pathlib`** and **`json`**: covered in the lesson "Files, JSON and CSV".

**`argparse`**: command-line interfaces. This one deserves a closer look.

### argparse: real command-line tools

A command-line program receives its arguments as a list of strings (`sys.argv`). Parsing them by hand gets messy fast. `argparse` does it for you, and generates `--help` and error messages for free.

```python
# greet.py
import argparse

parser = argparse.ArgumentParser(description="Say hello.")
parser.add_argument("name", help="who to greet")
parser.add_argument("--times", type=int, default=1, help="how many times")
parser.add_argument("--shout", action="store_true", help="use capitals")

args = parser.parse_args()
message = f"Hello, {args.name}!"
for _ in range(args.times):
    print(message.upper() if args.shout else message)
```

```bash
$ python greet.py Ada --times 2
Hello, Ada!
Hello, Ada!
$ python greet.py Ada --times two
usage: greet.py [-h] [--times TIMES] [--shout] name
greet.py: error: argument --times: invalid int value: 'two'
$ python greet.py --help
usage: greet.py [-h] [--times TIMES] [--shout] name

Say hello.

positional arguments:
  name           who to greet

options:
  -h, --help     show this help message and exit
  --times TIMES  how many times
  --shout        use capitals
```

- A name without dashes (`"name"`) is a **positional** argument: required, and identified by its position.
- A name with `--` is an **option**: optional, with a `default`.
- `type=int` converts the string for you and rejects bad input with a clear error.
- `action="store_true"` makes a **flag**: `True` if present, `False` if not.

Tools like `git` have **subcommands** (`git add`, `git commit`), each with its own arguments. `argparse` supports that with `add_subparsers`, which you'll use in the practice to build a to-do app's interface. A handy trick for testing: `parser.parse_args(["Ada", "--times", "2"])` parses a list you give it instead of the real command line.

## Third-party packages: pip, venv and uv

When the standard library doesn't have what you need, someone has usually published a package on **PyPI** (the Python Package Index). You install them with **pip**.

But don't install into your system's Python. Each project gets its own **virtual environment** (venv): a folder containing a private copy of Python and that project's packages, so two projects can use different versions of the same library without fighting.

```bash
$ python3 -m venv .venv            # create the environment in a folder called .venv
$ source .venv/bin/activate        # macOS/Linux (Windows: .venv\Scripts\activate)
(.venv) $ pip install requests
Successfully installed ... requests-2.32.5 ...
(.venv) $ python -c "import requests; print(requests.__version__)"
2.32.5
```

While the venv is active (your prompt shows `(.venv)`), `pip install` puts packages **inside `.venv`** (in its `site-packages` folder), and `python` uses them. Deactivate with `deactivate`. The `.venv` folder never goes into Git; you'll add it to `.gitignore` in the Git section.

**`uv`** is a newer tool that does the same jobs much faster and is becoming the default in many teams. `uv venv` creates the environment and `uv pip install requests` installs into it; `uv add requests` also records the dependency in your project file. The ideas are identical, so learn them with pip first, because that's what most documentation and answers online assume.

### Recording your dependencies

Other people (and future you, and your deployment server) need to know which packages your project uses.

- **`requirements.txt`**: the classic. A plain list, one package per line, often with versions: `requests==2.32.5`. Install everything with `pip install -r requirements.txt`.
- **`pyproject.toml`**: the modern standard file describing a Python project: its name, Python version and dependencies. Tools like `uv` and `pip` read it.
- A **lockfile** (such as `uv.lock`) records the *exact* version of every package, including the packages your packages depend on, so every install is identical. You don't edit it by hand; the tool writes it.

## Reading library documentation

You'll spend a lot of your career reading docs. A good routine for a new module:

1. **Read the overview and the first example.** They show the intended use.
2. **Find the function you need** and read its signature: parameters, defaults, what it returns, and what it raises.
3. **Try it in the Python shell** (the REPL) before using it in your program. `help(Counter.most_common)` shows the docstring right there.
4. **Check the version.** Docs pages have a version selector; make sure it matches your Python.

The official Python docs for each module in this lesson are linked in the resources. Get used to them; they're accurate, complete and free.

## Common mistakes

**`ModuleNotFoundError` for a package you installed.** You installed it in one environment and ran Python from another. Check that your venv is active, and that VS Code's selected interpreter is the `.venv` one. `python -m pip install ...` guarantees pip installs into the Python you're running.

**Shadowing a module with your own file name.** `random.py`, `json.py`, `test.py`, `email.py`: rename your file (and delete any `__pycache__` folder next to it).

**Script code running on import.** You imported `helpers.py` and it started asking for input. Move that code under `if __name__ == "__main__":`.

**Reinventing the standard library.** Writing your own word counter, date maths or argument parser. Search the docs first: "python count occurrences" leads straight to `Counter`.

## Recap

- A module is a `.py` file; a package is a folder of modules. `import` runs a module once and gives you access to its names.
- `__name__` is `"__main__"` when a file is run directly, and the module name when it's imported. Put script code under `if __name__ == "__main__":`.
- The standard library covers a lot: `random`, `datetime`, `collections`, `itertools`, `pathlib`, `json`, `argparse`. Check it before writing utilities.
- Use one virtual environment per project. With it active, `pip install` puts packages inside `.venv`. `uv` does the same, faster.
- Record dependencies in `requirements.txt` or `pyproject.toml`; a lockfile pins exact versions.
