import io
import sys

KNOWN = ("-l", "-w", "-c")


def counts(text: str) -> tuple[int, int, int]:
    """Return (lines, words, chars) for a piece of text."""
    return (text.count("\n"), len(text.split()), len(text))


def format_counts(text: str, options: list[str]) -> str:
    lines, words, chars = counts(text)
    picked = []
    if not options or "-l" in options:
        picked.append(lines)
    if not options or "-w" in options:
        picked.append(words)
    if not options or "-c" in options:
        picked.append(chars)
    return " ".join(str(n) for n in picked)


def main(argv: list[str], stdin, stdout, stderr) -> int:
    """A tiny wc. Results to stdout, errors to stderr, returns the exit code."""
    options = [a for a in argv if a.startswith("-")]
    names = [a for a in argv if not a.startswith("-")]

    for option in options:
        if option not in KNOWN:
            print(f"error: unknown option {option}", file=stderr)
            return 2

    if not names:
        print(format_counts(stdin.read(), options), file=stdout)
        return 0

    exit_code = 0
    for name in names:
        try:
            with open(name, encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"error: {name}: no such file", file=stderr)
            exit_code = 1
            continue
        print(f"{format_counts(text, options)} {name}", file=stdout)
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], sys.stdin, sys.stdout, sys.stderr))
