# Your machine, set up like an engineer's

Set up your own computer the way a working engineer would, and write down every step in a `SETUP.md` file as you go. From here on, every project in the course is built on this machine, so a clean setup now saves you hours later. It also gives you a record you can follow again on a new laptop or a work machine.

Plan on one to two evenings. Most of the time goes on installing things and fixing small surprises, which is part of the job.

## What you're building

A folder structure for all your course work, created entirely from the terminal:

```
~/projects/
├── se-course/
│   ├── setup-check/        ← this project
│   │   ├── .venv/          (not something you write: created by python3 -m venv)
│   │   ├── SETUP.md
│   │   ├── hello.py
│   │   └── test_hello.py
│   └── notes/
└── scratch/                ← a place for throwaway experiments
```

## Steps

### 1. Install Python and check it

Install Python 3.12 or newer (see "Your Python setup"). In a **new** terminal window, run:

```bash
$ python3 --version
Python 3.15.2
```

Paste your real output into `SETUP.md` under a heading `## Python`. If you hit `command not found`, write down what you did to fix it. That note is exactly what you'll want next time.

### 2. Build the folders from the terminal

Don't touch the Finder or File Explorer for this step. Use `cd`, `mkdir -p`, `touch`, `ls` and `pwd` from "The terminal". Copy every command you ran into `SETUP.md` under `## Folders`, in a ```` ```bash ```` block, so someone else could repeat it exactly. Finish with the output of `ls -a` inside `setup-check/`.

### 3. Create a virtual environment and install pytest

Inside `setup-check/`:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate        # Windows: .venv\Scripts\activate
(.venv) $ python -m pip install pytest
(.venv) $ which python             # Windows: where python
```

Record the `which python` output: it should point inside `.venv`.

### 4. Set up VS Code

Install VS Code and the Python extension, open the `setup-check` **folder**, and select the `.venv` interpreter. Take note of what the status bar shows and write it down.

### 5. One script, three ways

Write `hello.py` with a small pure function and a `__main__` block, for example:

```python
def greet(name: str) -> str:
    return f"Hello, {name.strip().title()}!"


if __name__ == "__main__":
    print(greet("  ada lovelace "))
```

Run it:

1. in the REPL (`python`, then `from hello import greet`, then call it),
2. from the terminal with `python hello.py`,
3. with the VS Code Run button.

Paste the output of each into `SETUP.md` and write one sentence on what was different about the REPL.

### 6. A passing test

Write `test_hello.py`:

```python
from hello import greet


def test_greet_cleans_the_name():
    assert greet("  ada lovelace ") == "Hello, Ada Lovelace!"
```

Run `pytest` from the terminal with the venv active and paste the output (it should end with `1 passed`). Then break `greet` on purpose, run `pytest` again, and read the failure. Put it back.

### 7. Your AI policy

Under `## How I'll use AI while learning`, write one paragraph **in your own words** (don't ask an AI to write it). Say when you'll use AI tools, what you'll ask them for, and what you won't let them do for you while a skill is new. "Learning like an engineer" has the evidence behind this.

## Checking your work

Go through the checklist below. A good `SETUP.md` is one that a classmate could follow on a fresh laptop without asking you anything.

## Stretch goals

- Install `uv` and recreate the environment with `uv venv` and `uv pip install pytest`. Note the time difference.
- Add a `requirements.txt` with `pip freeze > requirements.txt`, delete `.venv`, and rebuild it from the file.
- Turn on VS Code auto-save and format-on-save.
