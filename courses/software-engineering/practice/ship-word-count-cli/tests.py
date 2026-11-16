import io
import os
import tempfile

from solution import main


def run(argv, text=""):
    out, err = io.StringIO(), io.StringIO()
    code = main(argv, io.StringIO(text), out, err)
    return code, out.getvalue(), err.getvalue()


def test_counts_lines_words_and_chars_from_stdin():
    got = run([], "hello world\nbye\n")
    want = (0, "2 3 16\n", "")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_options_pick_which_counts_to_show():
    got = run(["-c", "-l"], "one two\nthree\n")
    want = (0, "2 14\n", "")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_empty_input_counts_zero():
    got = run([], "")
    want = (0, "0 0 0\n", "")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_unknown_option_goes_to_stderr_with_exit_code_2():
    got = run(["-x"], "text\n")
    want = (2, "", "error: unknown option -x\n")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_counts_each_file_and_reports_missing_ones():
    with tempfile.TemporaryDirectory() as tmp:
        a = os.path.join(tmp, "a.txt")
        with open(a, "w", encoding="utf-8") as f:
            f.write("hi\nthere you\n")
        missing = os.path.join(tmp, "missing.txt")
        got = run(["-w", missing, a])
        want = (1, f"3 {a}\n", f"error: {missing}: no such file\n")
    assert got == want, f"expected {want!r}, got {got!r}"
