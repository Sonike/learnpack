# Processes, memory and the operating system

## Why this matters

Every program you have written so far ran inside something: when you typed `python3 hello.py`, a whole chain of events happened before your first `print`. When your code goes to a server, that chain is all you have. The server has no screen and no one watching. It knows only whether your program started, what it wrote, and the number it returned when it finished. Learning to speak that language (streams, exit codes, environment variables, signals) is what turns a script into a tool other programs and other engineers can rely on.

## What an operating system does

An **operating system** (OS) is the program that runs all the other programs. Windows, macOS and Linux are operating systems. Most servers run Linux. The OS has three big jobs:

1. **Share the hardware.** Your laptop may have 8 CPU cores and hundreds of programs that want to run. The OS switches between them many times per second, so each one feels like it has the machine to itself.
2. **Keep programs apart.** Your browser can't read your Python program's memory, and a crash in one program doesn't take down the others.
3. **Give programs a simple interface to hardware.** Your code calls `open("notes.txt")`. It doesn't need to know whether the file lives on an SSD, a USB stick or a network drive. The OS handles that.

Programs ask the OS for things through **system calls**: "open this file", "give me more memory", "start another program". Python wraps these for you in functions like `open()` and modules like `os`.

## Processes

A **program** is a file on disk: `hello.py`, or the `python3` executable itself. A **process** is a program that is running. One program can run as many processes at once: open three terminal windows, run `python3` in each, and you have three Python processes.

Each process gets:

- a **PID** (process ID), a number the OS uses to name it,
- its own **memory**, which other processes can't touch,
- three open **streams** (more on these below),
- a copy of the **environment variables** of whoever started it,
- a **current working directory**, the folder relative paths are resolved from.

You can see your own process's details from Python:

```python
import os

print(os.getpid())   # 48213   (a different number every run)
print(os.getcwd())   # /Users/ada/projects/demo
```

In a terminal, `ps` lists processes. On macOS and Linux:

```bash
$ ps
  PID TTY           TIME CMD
48102 ttys001    0:00.05 -zsh
48213 ttys001    0:00.03 python3 demo.py
```

The shell (`zsh` here) is itself a process. When you type a command, the shell starts a new **child process** for it and waits for it to finish.

## The three standard streams

Every process starts with three streams already open. A **stream** is a channel you can read bytes or text from, or write to, one piece after another.

```
                 +------------------+
  stdin   ---->  |                  |  ---->  stdout
 (keyboard,      |     process      |        (normal output)
  a file,        |                  |  ---->  stderr
  a pipe)        +------------------+        (errors, diagnostics)
```

- **stdin** (standard input): where `input()` reads from. Usually the keyboard, but it can be a file or the output of another program.
- **stdout** (standard output): where `print()` writes. Usually the terminal.
- **stderr** (standard error): a second output, for error messages and diagnostics.

Why two outputs? So that the normal results and the complaints can go to different places. Here's a program that uses both:

```python
import sys

print("42 lines")                              # goes to stdout
print("warning: file was empty", file=sys.stderr)  # goes to stderr
```

In the terminal both appear on screen. But redirect stdout to a file and watch them split:

```bash
$ python3 count.py > result.txt
warning: file was empty
$ cat result.txt
42 lines
```

`>` sent stdout to `result.txt`, while stderr still came to the screen. That's the point: if another program reads your output, it gets clean results, and a person still sees the warnings. The `|` (pipe) does the same: `python3 count.py | sort` sends only stdout into `sort`.

> **Note:** `sys.stdin`, `sys.stdout` and `sys.stderr` are ordinary Python file-like objects. Anything that has `.write()` (and `.read()` for input) can stand in for them, including `io.StringIO`, an in-memory text buffer. That's how you test a command-line program without a real terminal.

```python
import io

fake_out = io.StringIO()
print("hello", file=fake_out)
print(repr(fake_out.getvalue()))   # 'hello\n'
```

## Exit codes

When a process finishes, it hands the OS one small number: its **exit code** (or exit status). The convention is simple:

- `0` means success.
- Anything else (usually `1` to `255`) means something went wrong. Many tools use `1` for a general error and `2` for "you used the command wrong" (bad arguments).

Your shell stores the last exit code in `$?`:

```bash
$ ls notes.txt
notes.txt
$ echo $?
0
$ ls missing.txt
ls: missing.txt: No such file or directory
$ echo $?
1
```

Exit codes are how programs talk to other programs. `git` hooks, CI pipelines, `&&` in the shell and deploy scripts all read them. A CI job that runs your tests passes or fails purely on the exit code of `pytest`. If your script prints "ERROR" but exits with `0`, every automated system will think it worked.

In Python, a script that reaches the end exits with `0`. An uncaught exception exits with `1`. To choose the code yourself, use `sys.exit`:

```python
import sys

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: greet NAME", file=sys.stderr)
        return 2
    print(f"Hello, {sys.argv[1]}!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

```bash
$ python3 greet.py
usage: greet NAME
$ echo $?
2
$ python3 greet.py Ada
Hello, Ada!
$ echo $?
0
```

This pattern, a `main()` that **returns** a code and one line that calls `sys.exit(main())`, is worth copying into every command-line tool you write. It keeps `main` testable: a test can call `main()` and check the number it returns, without the whole test run exiting.

Going one step further, pass `argv` and the streams in as arguments, and `main` becomes a plain function that a test can drive with `io.StringIO`. That's exactly what the practice exercise asks you to build.

## Command-line arguments

`sys.argv` is the list of words the process was started with. `sys.argv[0]` is the script name; the rest are the arguments:

```python
# args.py
import sys
print(sys.argv)
```

```bash
$ python3 args.py report.txt --verbose
['args.py', 'report.txt', '--verbose']
```

For anything bigger than a couple of arguments, use the standard `argparse` module, which you met in the file-organiser project. It builds the `--help` text and the "usage" errors (with exit code 2) for you.

## Environment variables

Every process carries a small dictionary of text settings called **environment variables**. A child process gets a copy of its parent's. Common ones are `HOME` (your home folder), `PATH` (the folders the shell searches for commands) and `LANG` (your language).

```python
import os

print(os.environ["HOME"])            # /Users/ada
print(os.environ.get("APP_MODE"))    # None (not set)
```

```bash
$ APP_MODE=dev python3 show_mode.py
dev
```

Writing `NAME=value` before a command sets the variable for that one process. Because each child gets a *copy*, a program can't change its parent shell's environment: `os.environ["X"] = "1"` inside Python is gone when Python exits.

Environment variables are how you configure a program without editing its code: the port to listen on, the database address, the API key. The next lesson, Configuration and secrets, is all about using them well.

## Signals: how Ctrl+C works

A **signal** is a tiny message the OS delivers to a process. When you press Ctrl+C in the terminal, the OS sends the running process the `SIGINT` ("interrupt") signal. Python turns that into a `KeyboardInterrupt` exception:

```python
import time

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping cleanly.")
```

```bash
$ python3 loop.py
^C
Stopping cleanly.
```

Two others you'll see in deploy logs:

- `SIGTERM`: "please shut down". Servers and container platforms send this before stopping your app, giving it a few seconds to finish requests and close files.
- `SIGKILL`: "stop now". It can't be caught. If you ever see a process "killed" with no chance to clean up, this is usually why (often because it used too much memory).

`kill PID` in the terminal sends `SIGTERM` to that process.

## Threads vs processes (the idea only)

A process can do more than one thing at a time by running several **threads**. Threads live *inside* one process and share its memory. Processes each have their own memory.

```
  Process A (own memory)          Process B (own memory)
  +-----------------------+       +-----------------------+
  | thread 1   thread 2   |       | thread 1              |
  |   \___ shared ___/    |       |                       |
  |        memory         |       |                       |
  +-----------------------+       +-----------------------+
```

Sharing memory makes threads cheap to start and quick to pass data between, but it also lets two threads change the same value at the same moment and corrupt it (a **race condition**). Separate processes are safer but heavier. For now, the important thing is the vocabulary: when a web server says it runs "4 workers", it usually means 4 processes, each handling requests independently. You won't write threaded code in this course.

## Memory: the stack and the heap

When a process runs, the OS gives it memory, and the language runtime organises that memory into two main areas.

The **call stack** holds one **frame** for each function call that hasn't finished yet. A frame holds that call's local variables. Call a function and a frame is pushed on top; return and it's popped off. You saw this in the recursion lesson:

```
factorial(3) calls factorial(2) calls factorial(1)

   top -> | factorial(1): n=1 |
          | factorial(2): n=2 |
          | factorial(3): n=3 |
          | <module>          |
```

The stack is small and fixed in size. Recurse too deep and you run out:

```python
def forever(n):
    return forever(n + 1)

forever(0)
# RecursionError: maximum recursion depth exceeded
```

Python stops you at about 1,000 frames by default so the process doesn't crash outright.

The **heap** is the large pool where objects live: every list, dict, string and instance of your classes. Variables on the stack are just *names that point at* objects on the heap. When nothing points at an object any more, Python's **garbage collector** frees its memory for reuse.

```python
def make_list():
    items = [1, 2, 3]   # the list lives on the heap; 'items' is a name in this frame
    return items        # the frame goes away, but the list survives: we returned it

nums = make_list()
print(nums)   # [1, 2, 3]
```

You don't manage memory by hand in Python. But you can still run out of it: read a 20 GB log file with `f.read()` and the whole thing has to fit on the heap. Looping `for line in f:` keeps only one line in memory at a time. When a server process gets killed for using too much memory, the cause is nearly always something like that.

## Common mistakes

**Printing errors to stdout.** If your tool prints `Error: file not found` with `print()`, anyone piping your output into another program now has an error message mixed into their data. Put errors on `sys.stderr`.

**Exiting with 0 after a failure.** Catching an exception, printing a message, and then falling off the end of the script exits with `0`. CI goes green, the deploy continues, and nobody notices. Return a non-zero code whenever the job didn't get done.

**Calling `sys.exit()` deep inside your code.** `sys.exit` raises a `SystemExit` exception. Called from a helper function, it makes the helper impossible to test and surprising to reuse. Return codes up to `main` and exit in one place.

**Expecting `os.environ` changes to stick.** Setting a variable inside Python changes only that process and its children. Set it in the shell (`export NAME=value`) or in your deploy settings instead.

**Reading the error.** A `RecursionError` means the stack filled up: look for recursion with no base case, or a base case that's never reached. A process that dies with `Killed` and exit code `137` (128 + 9, the number of `SIGKILL`) almost always ran out of memory.

> **Try it:** In the practice editor, write a function that prints one line to `sys.stdout` and one to `sys.stderr`, and returns `3`. Then call it with two `io.StringIO` objects instead of the real streams and print what each one captured.

## Recap

- The OS shares the hardware, keeps programs apart and gives them a simple interface through system calls.
- A process is a running program with a PID, its own memory, three streams, a copy of the environment and a working directory.
- stdout is for results, stderr for errors and diagnostics. Keep them separate so programs can be chained.
- Exit code `0` means success; anything else means failure, and automated tools trust it completely. Return codes from `main()` and call `sys.exit(main())` once.
- Environment variables configure a process from outside; children get a copy.
- Signals such as `SIGINT` (Ctrl+C) and `SIGTERM` (shut down) let the OS ask a process to stop.
- Threads share a process's memory; processes don't. The stack holds function frames; the heap holds your objects.
