# A `wc`-style command-line tool

Real command-line tools follow three rules: results go to **stdout**, errors go to **stderr**, and the **exit code** says whether it worked. You'll build a small version of the Unix `wc` (word count) tool that follows all three.

To make it testable, `main` doesn't use `sys.argv`, `sys.stdin` and friends directly. They're passed in:

```python
def main(argv: list[str], stdin, stdout, stderr) -> int:
```

- `argv`: the command-line arguments **without** the program name, for example `["-l", "notes.txt"]`.
- `stdin`: a text stream to read from when no file names are given (call `stdin.read()`).
- `stdout`, `stderr`: text streams to write to (use `print(..., file=stdout)`).
- Return the exit code as an `int`.

## Rules

1. **Counts.** For a piece of text: lines = `text.count("\n")`, words = `len(text.split())`, chars = `len(text)`.
2. **Options.** `-l`, `-w` and `-c` choose which counts to show. With no options, show all three. Counts are always shown in the order lines, words, chars, separated by single spaces.
3. **Unknown option.** Any other argument starting with `-` is an error: write `error: unknown option <arg>` to stderr, write nothing to stdout, and return `2`.
4. **No file names:** count `stdin` and print one line with the counts.
5. **File names** (any argument not starting with `-`): for each file in order, print the counts, a space, and the file name. If a file doesn't exist, write `error: <name>: no such file` to stderr, carry on with the next file, and return `1` at the end.
6. Otherwise return `0`.

## Examples

```python
import io
out, err = io.StringIO(), io.StringIO()

main([], io.StringIO("hello world\nbye\n"), out, err)   # returns 0
out.getvalue()   # '2 3 16\n'

main(["-w"], io.StringIO("one two three"), out2, err2)  # returns 0
out2.getvalue()  # '3\n'

main(["-x"], io.StringIO(""), out3, err3)               # returns 2
err3.getvalue()  # 'error: unknown option -x\n'
```

With a file `a.txt` containing `"hi\n"`:

```python
main(["a.txt", "missing.txt"], io.StringIO(""), out, err)  # returns 1
out.getvalue()  # '1 1 3 a.txt\n'
err.getvalue()  # 'error: missing.txt: no such file\n'
```
