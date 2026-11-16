# Files, folders and paths

## Why this matters

`FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'` is one of the first errors every programmer meets, usually when the file is sitting right there on the screen. The cause is almost always a path: the program looked in a different folder from the one you were thinking of. Once you understand how the filesystem is laid out and how paths are resolved, that error turns from a mystery into a two-second fix. Every later topic (running scripts, Git, configuration, deploying) assumes you can say exactly where a file is.

## The filesystem is a tree

Storage holds thousands of files, organised into **folders** (also called **directories**; the words mean the same thing). Folders can contain files and other folders, which contain more, and so on. Drawn out, it looks like an upside-down tree:

```
/                              ← the root: the top of the tree
├── Applications/
├── Users/
│   └── ada/                   ← ada's home directory
│       ├── Desktop/
│       ├── Documents/
│       │   └── cv.pdf
│       └── projects/
│           ├── app/
│           │   ├── main.py
│           │   └── data/
│           │       └── scores.csv
│           └── notes.txt
└── tmp/
```

- The **root** is the single folder at the very top. On macOS and Linux it's written `/`.
- Every file has exactly one **parent** folder, the one it's directly inside. The parent of `main.py` is `app`.
- Your **home directory** is the folder that belongs to your user account: `/Users/ada` on macOS, `/home/ada` on Linux, `C:\Users\ada` on Windows. Your Desktop and Documents folders live inside it. The shortcut `~` means "my home directory" in the terminal.

> **Note:** Windows has one tree per drive (`C:\`, `D:\`) and uses backslashes `\` between names. macOS and Linux have a single tree starting at `/` and use forward slashes `/`. Servers almost all run Linux, so this course writes paths the `/` way. Python accepts `/` on Windows too.

## Paths: the address of a file

A **path** is the list of folders you walk through to reach a file, joined with `/`.

### Absolute paths

An **absolute path** starts at the root, so it means the same thing no matter where you are:

```
/Users/ada/projects/app/data/scores.csv
```

Read it as directions: start at `/`, go into `Users`, then `ada`, then `projects`, `app`, `data`, and there's `scores.csv`. Absolute paths always start with `/` (or a drive letter like `C:\` on Windows).

### The current working directory

Every running program, including your terminal, has a **current working directory** (often shortened to *cwd*): the folder it's "standing in" right now. When you open a terminal, it usually starts in your home directory. When you run a Python script, its cwd is whatever folder the terminal was in when you ran it (not necessarily the folder the script lives in!). That last point causes a lot of `FileNotFoundError`s.

### Relative paths

A **relative path** doesn't start with `/`. It's directions *from the current working directory*:

```
cwd:            /Users/ada/projects/app
relative path:  data/scores.csv
means:          /Users/ada/projects/app/data/scores.csv
```

Relative paths are shorter and let a project work wherever it's copied, because they don't bake in `/Users/ada`. But they only work if the cwd is what you expect.

### `.` and `..`

Two special names appear in every folder:

- `.` means "this folder". `./main.py` is the same as `main.py`.
- `..` means "the parent folder", one level up.

```
cwd:              /Users/ada/projects/app
../notes.txt   →  /Users/ada/projects/notes.txt
../../Documents/cv.pdf  →  /Users/ada/Documents/cv.pdf
./data/../main.py       →  /Users/ada/projects/app/main.py
```

Work these out by hand: start from the cwd, split the path at each `/`, and for every piece step into that folder (`..` steps up, `.` stays put). At the root, `..` has nowhere to go and stays at `/`. You'll write exactly this logic in the first exercise.

## Paths in Python

Python's standard library has a module for paths called **`pathlib`**. A `Path` object knows how to join and pick apart paths correctly on every operating system:

```python
from pathlib import Path

p = Path("/home/ada/projects/app/main.py")
print(p.name)     # main.py
print(p.stem)     # main
print(p.suffix)   # .py
print(p.parent)   # /home/ada/projects/app

notes = Path("/home/ada") / "notes" / "todo.txt"   # / joins path pieces
print(notes)      # /home/ada/notes/todo.txt
```

Two more you'll use constantly:

```python
from pathlib import Path

print(Path.cwd())    # the current working directory, e.g. /home/ada/projects/app
print(Path.home())   # your home directory, e.g. /home/ada
print(Path("data/scores.csv").resolve())   # the absolute path that relative path points to
```

When a file "isn't found", print `Path.cwd()` and `Path("your/path").resolve()`. The answer is almost always right there: the program is standing in a different folder from the one you assumed.

> **Try it:** in the practice editor, run `from pathlib import Path; print(Path.cwd())`. That's the folder your code runs in on this platform.

## File names and extensions

A file name like `report.pdf` has two parts: the **stem** (`report`) and the **extension** (`.pdf`), the part after the last dot. Extensions are only a naming convention. They tell your operating system which app to open the file with and tell people what to expect, but they don't change what's inside. Rename `photo.jpg` to `photo.txt` and the bytes are identical; your text editor will just show nonsense.

Some names to know:

```
main.py           stem "main",        extension ".py"
archive.tar.gz    stem "archive.tar", extension ".gz"   (only the last dot counts)
Makefile          stem "Makefile",    no extension
.gitignore        stem ".gitignore",  no extension      (a hidden file, see below)
```

`pathlib` follows exactly these rules (`Path("archive.tar.gz").suffixes` gives `['.tar', '.gz']` if you want all of them). The second exercise has you write `stem`/`suffix` yourself.

## Text files and binary files

Every file is bytes. The difference is how those bytes are meant to be read:

- A **text file** holds characters in an encoding (usually UTF-8, from "How computers run code"). Python files, `.txt`, `.csv`, `.json`, `.md` and configuration files are text. Any text editor can open them, and Git can show line-by-line changes in them.
- A **binary file** holds bytes in some other format that only a specific program understands: images, PDFs, ZIP archives, compiled programs, Word documents. Open one in a text editor and you see gibberish.

As a programmer you'll spend most of your time in text files, which is why plain text is the format of choice for code, configuration and notes.

## Hidden files

On macOS and Linux, any file or folder whose name **starts with a dot** is **hidden**: file browsers and the plain `ls` command don't show it. That's the whole rule; there's no special flag. Hidden files are usually settings you don't want cluttering your view:

```
.gitignore     which files Git should ignore
.env           secret settings such as API keys (never share this one)
.venv/         a Python virtual environment (see "Your Python setup")
.git/          the whole history of a Git project
```

You'll see them in the terminal with `ls -a` ("all"). In the macOS Finder, press Cmd+Shift+. to toggle them. Windows marks hidden files with a file attribute instead of the name, but the dot-files from programming tools still show up there.

## Why spaces in paths cause pain

`My Documents/cv final (2).pdf` is a legal path, but the terminal splits commands on spaces, so it reads this as three separate things: `My`, `Documents/cv`, and so on. You have to wrap the path in quotes or escape each space with a backslash:

```bash
cd My Documents
# cd: string not in pwd: My     (zsh)  or   bash: cd: My: No such file or directory

cd "My Documents"     # works
cd My\ Documents      # also works
```

The professional habit: name your own files and folders in lowercase with dashes or underscores and no spaces (`cv-final.pdf`, `data_2026.csv`). You'll save yourself countless quoting bugs.

Case is a second trap. Linux treats `Data.csv` and `data.csv` as two different files; macOS and Windows normally treat them as the same. Code that works on your Mac can fail on a Linux server because of one capital letter. Pick a convention and stick to it.

## Common mistakes

**Assuming the cwd is the script's folder.** You run `python app/main.py` from `/Users/ada/projects`, and `open("data/scores.csv")` looks for `/Users/ada/projects/data/scores.csv`, not inside `app/`. The error:

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/scores.csv'
```

tells you the exact path it tried. Compare it with where the file actually is. Either run the script from the right folder, or build the path from the script's own location: `Path(__file__).parent / "data" / "scores.csv"`.

**Hard-coding your own absolute path.** `/Users/ada/projects/app/data.csv` works on your laptop and nowhere else. Prefer paths relative to the project.

**Gluing paths with string `+`.** `folder + "/" + name` easily produces `data//file.csv` or forgets the slash. Use `Path(folder) / name`.

**Trusting the extension.** A file called `data.csv` might be saved with semicolons, a different encoding, or might not be a CSV at all. Open it and look.

## Recap

- The filesystem is a **tree** that starts at the **root** `/`. Your **home directory** (`~`) holds your own files.
- An **absolute path** starts at `/` and means the same thing everywhere. A **relative path** starts from the **current working directory**.
- `.` is "this folder", `..` is "the parent". Resolve a path by walking it piece by piece.
- An **extension** is just the end of the name after the last dot. It doesn't change the contents.
- **Text files** are characters in an encoding; **binary files** need a specific program.
- Names starting with `.` are **hidden**. Avoid spaces in names, and remember Linux cares about capitals.
- Use `pathlib.Path` in Python, and print `Path.cwd()` when a file "isn't there".
