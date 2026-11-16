import contextlib
import io

from solution import build_parser


def rejected(argv):
    """True if argparse refuses argv (it raises SystemExit). Hides argparse's error text."""
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            build_parser().parse_args(argv)
    except SystemExit:
        return True
    return False


def test_add_takes_text_with_normal_priority_by_default():
    args = build_parser().parse_args(["add", "Buy milk"])
    got = (args.command, args.text, args.priority)
    want = ("add", "Buy milk", "normal")
    assert got == want, f"expected {want!r}, got {got!r}"


def test_add_accepts_a_priority():
    args = build_parser().parse_args(["add", "Pay rent", "--priority", "high"])
    assert args.priority == "high", f"expected 'high', got {args.priority!r}"


def test_list_has_an_all_flag():
    parser = build_parser()
    plain = parser.parse_args(["list"])
    everything = parser.parse_args(["list", "--all"])
    got = (plain.command, plain.all, everything.all)
    want = ("list", False, True)
    assert got == want, f"expected {want!r}, got {got!r}"


def test_done_converts_the_id_to_an_int():
    args = build_parser().parse_args(["done", "3"])
    assert args.command == "done", f"expected 'done', got {args.command!r}"
    assert args.id == 3, f"expected the int 3, got {args.id!r}"


def test_rejects_bad_input():
    for argv in (["done", "abc"], ["add", "x", "--priority", "urgent"], [], ["fly"]):
        assert rejected(argv), f"expected argparse to reject {argv!r}"
