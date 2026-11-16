import io
import sys


def counts(text: str) -> tuple[int, int, int]:
    """Return (lines, words, chars) for a piece of text."""
    # TODO: lines = number of "\n", words = len(text.split()), chars = len(text)
    return (0, 0, 0)


def main(argv: list[str], stdin, stdout, stderr) -> int:
    """A tiny wc. Results to stdout, errors to stderr, returns the exit code."""
    # TODO: split argv into options (start with "-") and file names
    # TODO: reject unknown options: message to stderr, return 2
    # TODO: no file names -> count stdin.read() and print one line
    # TODO: file names -> print counts + " " + name for each; missing file -> stderr, exit code 1
    return 0


if __name__ == "__main__":
    out, err = io.StringIO(), io.StringIO()
    code = main(["-l", "-w"], io.StringIO("hello world\nbye\n"), out, err)
    print("exit code:", code)
    print("stdout:", repr(out.getvalue()))
    print("stderr:", repr(err.getvalue()))
