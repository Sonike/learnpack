# The terminal

## Why this matters

Almost every tool a software engineer uses runs from the terminal: Python, Git, the test runner, package installers, deploy tools, and the servers your code will eventually run on, which usually have no mouse or windows at all. Job descriptions rarely say "terminal" because they assume it. You only need about twenty commands and a handful of ideas to be comfortable, and that's what this lesson gives you.

## Terminal, shell and prompt

Three words that get mixed up:

- The **terminal** is the window you type into: Terminal on macOS, Windows Terminal, the terminal panel inside VS Code. It shows text and passes your keystrokes on.
- The **shell** is the program running *inside* the terminal that reads your commands and runs them. macOS uses **zsh** by default; most Linux systems use **bash**. For everything in this lesson they behave the same.
- The **prompt** is the bit of text the shell prints when it's ready for your next command. It often shows your user name, computer and current folder, and ends in `$` or `%`:

```
ada@laptop ~/projects %
```

In this course, a `$` at the start of a line means "type the rest of this line"; don't type the `$` itself. Lines without `$` are what the computer prints back.

> **Note:** On Windows, install **WSL** (Windows Subsystem for Linux) or use **Git Bash** so you have a bash shell. The older Windows shells (Command Prompt and PowerShell) use different commands, and most tutorials, servers and job tools assume bash or zsh.

## Commands, arguments and flags

Every command has the same shape:

```
command  -flags  arguments
   ls     -l     projects
```

- The **command** is the program to run (`ls`, `cd`, `python3`, `git`).
- **Arguments** are what it works on: usually file or folder names.
- **Flags** (also called **options**) change how it behaves. Short flags are one dash and one letter (`-l`), and can often be combined (`-la` means `-l -a`). Long flags use two dashes and a word (`--all`).

Spaces separate the parts, which is why a folder called `My Documents` needs quotes: `"My Documents"`. You'll write a parser that splits commands this way in the second exercise.

## Finding your way around

These three commands answer "where am I, what's here, and how do I move?"

```bash
$ pwd
/Users/ada
```

`pwd` (**p**rint **w**orking **d**irectory) shows the current working directory: the folder the shell is standing in. Relative paths are resolved from here.

```bash
$ ls
Desktop    Documents    projects
$ ls -a
.    ..    .zshrc    Desktop    Documents    projects
$ ls -l projects
drwxr-xr-x  4 ada  staff  128 Nov 13 09:12 app
-rw-r--r--  1 ada  staff  412 Nov 12 18:40 notes.txt
```

`ls` (**l**i**s**t) shows what's in a folder: the current one, or the one you name. `-a` includes hidden files (names starting with `.`), and `-l` gives the long format: permissions (a `d` at the start means directory), owner, size in bytes, and last-modified date.

```bash
$ cd projects
$ pwd
/Users/ada/projects
$ cd ..
$ pwd
/Users/ada
$ cd ~/projects/app
$ cd -
/Users/ada
```

`cd` (**c**hange **d**irectory) moves you. It takes a relative or absolute path, and all the path rules from "Files, folders and paths" apply: `..` goes up, `~` is home, and `cd` on its own goes home. `cd -` jumps back to the previous folder.

## Creating, copying, moving and deleting

```bash
$ mkdir notes                  # make a directory
$ mkdir -p notes/2026/nov      # -p: make any missing parent folders too, no error if it exists
$ touch notes/todo.txt         # create an empty file (or update the date of an existing one)
$ cp notes/todo.txt backup.txt # copy a file: cp SOURCE DESTINATION
$ cp -r notes notes-copy       # copy a whole folder: -r means recursive (everything inside)
$ mv backup.txt old.txt        # move, which is also how you rename
$ mv old.txt notes/            # move into a folder
$ rm notes/old.txt             # remove a file
$ rm -r notes-copy             # remove a folder and everything in it
```

None of these print anything when they work. That's normal: in the terminal, silence means success. Use `ls` to check.

### `rm` has no undo

`rm` doesn't move files to the Trash or Recycle Bin. They're gone. `rm -r` deletes an entire folder tree, and `rm -rf` does it without asking about anything. Before you press Enter on an `rm`:

1. Run `pwd` and make sure you're where you think you are.
2. Run `ls` with the same path first, to see exactly what will be removed.
3. Never paste an `rm` command you don't fully understand, whether from a forum or an AI tool.

## Getting help

You don't memorise flags. You look them up:

```bash
$ ls --help        # many commands print a summary (works on Linux; macOS ls doesn't support it)
$ man ls           # the full manual page; press q to quit, / to search, Space for the next page
$ python3 --help
usage: python3 [option] ... [-c cmd | -m mod | file | -] [arg] ...
```

`man` (**man**ual) works for almost every built-in command on macOS and Linux. Get in the habit of reading the first screen of a man page before searching the web.

## Looking inside files

```bash
$ cat notes.txt           # print the whole file
$ head -n 5 scores.csv    # the first 5 lines
$ tail -n 5 server.log    # the last 5 lines
$ less server.log         # scroll through a long file; q to quit, / to search
$ grep "error" server.log # print only the lines containing "error"
$ grep -i "error" server.log   # -i: ignore case (Error, ERROR, error)
$ grep -rn "TODO" .            # -r: search every file under this folder, -n: show line numbers
```

`grep` is the one you'll use most at work: "where in this codebase is that function called?" is `grep -rn "function_name" .`.

## Pipes and redirection

Each command reads input and writes output as text. The shell lets you connect them.

### Pipes: `|`

A **pipe** sends the output of one command into the input of the next:

```bash
$ ls -la | grep py
-rw-r--r--  1 ada  staff  1203 Nov 13 09:12 main.py
-rw-r--r--  1 ada  staff   388 Nov 13 09:15 test_main.py
$ cat server.log | grep -i error | head -n 3
```

Read the second line left to right: print the log, keep only the error lines, show the first three. Small tools chained together is the core idea of the Unix shell.

### Redirection: `>` and `>>`

```bash
$ ls > files.txt          # write the output to files.txt instead of the screen
$ echo "first" > log.txt  # > replaces the file's contents (creating it if needed)
$ echo "second" >> log.txt   # >> appends to the end
$ cat log.txt
first
second
```

Be careful with `>`: it wipes the file before writing. `ls -la | grep py > out.txt` lists everything including hidden files, keeps the lines containing "py", and saves them to `out.txt`, replacing whatever was there.

## Working faster: tab completion and history

- **Tab completion:** type the start of a file or folder name and press Tab, and the shell finishes it. Press Tab twice to see all matches. This also avoids typos and quoting problems.
- **History:** the Up arrow brings back previous commands. `Ctrl+R` searches your history as you type. `history` lists it.
- **Stop a running command:** `Ctrl+C`. Use it when something hangs or you started the wrong thing.
- **Clear the screen:** `clear` or `Ctrl+L`.

## Running programs

Any program on your computer can be run from here by name, with arguments:

```bash
$ python3 --version
Python 3.13.1
$ python3 hello.py
Hello, world!
```

The shell finds programs by looking through a list of folders stored in an **environment variable** called `PATH`. When you see `command not found: python3`, it means no folder on your `PATH` contains a program with that name. Either it isn't installed, or it was installed somewhere the shell doesn't look. You'll fix exactly this in "Your Python setup".

## Common mistakes

**Running a command in the wrong folder.** Most "it can't find my file" problems are this. `pwd` first.

**Forgetting quotes around names with spaces.**

```bash
$ cd My Documents
cd: string not in pwd: My
```

The shell saw two arguments. Use `cd "My Documents"` or Tab completion.

**Typing the `$`.** `$ ls` with the dollar gives `command not found: $`. The `$` is the prompt in instructions, not part of the command.

**Using `>` when you meant `>>`.** Your log file now has one line. There's no undo for this either.

**Reading `Permission denied`.** You're trying to change something your user doesn't own (system folders, often). Don't reach for `sudo` (run as administrator) to make the error go away unless you understand why you need it; it's usually a sign you're in the wrong place.

**Pasting commands from the internet or an AI tool without reading them.** Ask the AI to *explain* a command flag by flag before you run it. That's how you learn it, and how you avoid the one that deletes your home folder.

## Recap

- The **terminal** shows text; the **shell** (zsh or bash) runs your commands; the **prompt** says it's ready.
- Commands look like `command -flags arguments`. Quote anything with spaces.
- Navigate with `pwd`, `ls` (`-a`, `-l`) and `cd` (`..`, `~`, `-`).
- Change things with `mkdir -p`, `touch`, `cp -r`, `mv` and `rm` (no undo, check first).
- Get help with `man` and `--help`. Read files with `cat`, `head`, `tail`, `less`, and search them with `grep`.
- `|` pipes output into the next command; `>` overwrites a file, `>>` appends.
- Tab completes, Up and Ctrl+R recall history, Ctrl+C stops.
