# Your Python setup

## Why this matters

You can do every exercise in this course in the built-in editor, but real work happens on your own machine: your projects, your portfolio, and the take-home tasks employers send. A clean setup saves you hours of "it works in one place but not another". The most common beginner blocker isn't code at all; it's `pip install` "working" and the import still failing. By the end of this lesson you'll know why that happens and how to never hit it.

## Install Python

Python is a program like any other: the **interpreter** from "How computers run code". You install it once and then run your files with it.

- **macOS and Windows:** download the latest installer from python.org (linked below). On Windows, tick **"Add python.exe to PATH"** on the first screen of the installer; it saves a lot of trouble.
- **Linux:** Python is usually installed already. Use your package manager if you need a newer version.

Any version from **3.12** upwards works for this course. The newest release at the time of writing is 3.15; the in-browser editor runs 3.13, so the exercises only use features that work in 3.12 and later.

Check it from the terminal:

```bash
$ python3 --version
Python 3.15.2
```

On Windows the command is often `python` or `py` instead of `python3`. If you get `command not found` (or Windows opens the Microsoft Store), Python isn't on your `PATH`: the list of folders the shell searches for programs. Re-run the installer with the PATH option ticked, then open a **new** terminal window; old windows don't see the change.

## Two ways to run Python: the REPL and a file

### The REPL

Type `python3` on its own and you get an interactive prompt, `>>>`:

```bash
$ python3
Python 3.15.2 (main, ...) on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 2 + 3
5
>>> name = "Ada"
>>> name.upper()
'ADA'
>>> exit()
```

This is the **REPL**: it **R**eads a line, **E**valuates it, **P**rints the result, and **L**oops back for the next. It's perfect for quick experiments: "what does `.upper()` do?", "what's `7 // 2`?". Notice it shows the value of each expression automatically, without `print`. Everything you type disappears when you `exit()` (or press Ctrl+D on macOS/Linux, Ctrl+Z then Enter on Windows).

### Running a file

For anything you want to keep, write a **script**: a `.py` file you run from top to bottom.

```python
# hello.py
name = "Ada"
print(f"Hello, {name}!")
name.upper()          # computed, then thrown away: a script doesn't print values for you
```

```bash
$ python3 hello.py
Hello, Ada!
```

Only `print` produces output in a script. The `name.upper()` line runs but shows nothing, which is a common surprise after using the REPL.

The `if __name__ == "__main__":` block you'll see at the bottom of every exercise starter is a Python convention: the code inside runs when you run the file directly, but not when another file (like the tests) imports it. That's why the Run button shows your experiments and the Check button doesn't.

## VS Code

You need a code editor. **VS Code** is free, runs everywhere, and is what most of the industry uses. After installing it:

1. Open the Extensions view (the four-squares icon) and install **Python** by Microsoft. It adds syntax checking, autocomplete, a debugger and a Run button.
2. Open a **folder**, not a single file: File → Open Folder. VS Code treats that folder as your project, and its built-in terminal (View → Terminal) starts in it.
3. Look at the bottom-right status bar (or run "Python: Select Interpreter" from the Command Palette, Cmd/Ctrl+Shift+P). This is which Python VS Code uses. Remember this setting; it matters in a minute.

Turn on **auto-save** (File → Auto Save) so you never run an old version of your file by accident.

## Packages and pip

Python comes with a large **standard library**: modules like `pathlib`, `json` and `re` that are always available. Everything else is a **package** written by someone else and published on **PyPI** (the Python Package Index). You install packages with **pip**:

```bash
$ python3 -m pip install requests
Successfully installed certifi-... requests-...
```

Writing `python3 -m pip` instead of plain `pip` guarantees you're installing into the same Python you'll run. Hold on to that idea.

## Virtual environments

If every project installs its packages into one shared Python, they collide: project A needs version 1 of a package, project B needs version 2, and upgrading for one breaks the other. A **virtual environment** (venv) is a private folder of packages for a single project, plus a copy of the `python` command that uses it.

```bash
$ cd ~/projects/my-app
$ python3 -m venv .venv          # create it, in a hidden folder called .venv
$ source .venv/bin/activate      # turn it on (macOS/Linux)
(.venv) $                        # the prompt now shows it's active
```

On Windows, activate with `.venv\Scripts\activate` instead.

While it's active, `python` and `pip` mean the ones inside `.venv`:

```bash
(.venv) $ which python
/Users/ada/projects/my-app/.venv/bin/python
(.venv) $ pip install pytest
(.venv) $ deactivate             # turn it off
$
```

What the venv isolates is the **installed packages** (and which interpreter runs). It doesn't copy your code or change your files. The rules:

- One venv per project, in the project folder, named `.venv`.
- Never commit `.venv` to Git (you'll add it to `.gitignore` in the Git section). Instead, list your packages in a `requirements.txt` file so anyone can recreate it: `pip freeze > requirements.txt`, and later `pip install -r requirements.txt`.
- If a venv gets into a mess, delete the folder and make a new one. It's disposable.

In VS Code, select the `.venv` interpreter (step 3 above) so the Run button and the editor's import checks use the same packages as your terminal.

## uv: the faster modern tool

You'll increasingly see **uv** in projects and job postings. It's a single fast tool that installs Python versions, creates virtual environments and installs packages:

```bash
$ uv venv                 # creates .venv
$ uv pip install pytest   # installs into it, much faster than pip
$ uv run python hello.py  # runs using the project's environment
```

It does the same jobs as `venv` and `pip`, and it's well worth adopting. Learn the `venv` + `pip` way first, though: it's what most documentation, error messages and Stack Overflow answers assume, so you'll need it to read other people's instructions.

## Running the course tests on your machine

Every code exercise here is checked by a hidden `tests.py` full of plain `test_*` functions that use `assert`. The standard Python test runner, **pytest**, runs those unchanged. To practise locally:

```bash
(.venv) $ pip install pytest
(.venv) $ ls
solution.py    tests.py
(.venv) $ pytest tests.py
============================= test session starts ==============================
collected 4 items

tests.py ....                                                            [100%]

============================== 4 passed in 0.01s ===============================
```

On its own, `pytest` only collects files named `test_*.py` or `*_test.py`, so for a file called `tests.py` you name it, as above. Each dot is a passing test. A failure prints an `F` and then the exact assertion that failed, with the values involved. You'll learn to write tests yourself in the testing section.

## The edit → run → check loop

Your work rhythm from now on:

1. Read the task and **predict** what your code should do with the example input.
2. Write the code.
3. **Run** it with your own examples (the `__main__` block) and compare with your prediction.
4. **Check** it against the tests.
5. When a test fails, read its message; it says what was expected and what you returned. Fix, and go back to 3.

The first exercise in this lesson is tiny on purpose. The point is to go round this loop once, start to finish.

## Common mistakes

**`pip install` worked, but `import` fails.**

```
ModuleNotFoundError: No module named 'requests'
```

You installed the package into one Python and ran your code with another. Usually the venv wasn't active in the terminal where you installed, or VS Code is set to a different interpreter. Check with `which python` (macOS/Linux) or `where python` (Windows) in the terminal and the interpreter in VS Code's status bar; they should both point inside `.venv`. Using `python -m pip` with the same `python` you run avoids this entirely.

**Typing Python into the shell, or shell commands into Python.**

```
>>> pip install pytest
  File "<stdin>", line 1
    pip install pytest
        ^^^^^^^
SyntaxError: invalid syntax
```

The `>>>` prompt means you're inside Python. `exit()` first, then run the shell command.

**Forgetting to activate the venv** in a new terminal window. Each new terminal starts without it. Look for `(.venv)` in the prompt.

**Running an unsaved file.** The editor shows a dot on the tab when there are unsaved changes. Turn on auto-save.

**Using `sudo pip install`.** Installing packages as an administrator into the system Python can break tools your operating system relies on. Use a venv instead.

## Recap

- Install Python 3.12+ and check with `python3 --version`. `command not found` means it's not on your `PATH`.
- The **REPL** (`python3`) is for experiments and shows values automatically; **scripts** (`python3 file.py`) run top to bottom and only show what you `print`.
- Use **VS Code** with the Python extension, open folders not files, and select your project's interpreter.
- **pip** installs packages from PyPI. A **virtual environment** (`python3 -m venv .venv`, then activate) gives each project its own packages. **uv** is the fast modern tool for the same jobs.
- `ModuleNotFoundError` after a successful install means two different Pythons. Make the terminal and the editor use the same one.
- **pytest** runs the course's tests on your machine.
