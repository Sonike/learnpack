from solution import resolve_conflict

CONFLICTED = (
    "def greet(name):\n"
    "<<<<<<< HEAD\n"
    '    greeting = "Hello"\n'
    "=======\n"
    '    greeting = "Hi there"\n'
    ">>>>>>> feature/friendlier-greeting\n"
    '    return f"{greeting}, {name}!"\n'
)


def raises_value_error(text, choose="ours"):
    try:
        resolve_conflict(text, choose)
    except ValueError:
        return True
    return False


def test_keeps_ours():
    got = resolve_conflict(CONFLICTED, "ours")
    want = 'def greet(name):\n    greeting = "Hello"\n    return f"{greeting}, {name}!"\n'
    assert got == want, f"expected {want!r}, got {got!r}"


def test_keeps_theirs():
    got = resolve_conflict(CONFLICTED, "theirs")
    want = 'def greet(name):\n    greeting = "Hi there"\n    return f"{greeting}, {name}!"\n'
    assert got == want, f"expected {want!r}, got {got!r}"


def test_keeps_both_ours_first():
    got = resolve_conflict("<<<<<<< HEAD\na\n=======\nb\nc\n>>>>>>> main\n", "both")
    want = "a\nb\nc\n"
    assert got == want, f"expected {want!r}, got {got!r}"


def test_resolves_several_blocks_and_leaves_clean_text_alone():
    text = "top\n<<<<<<< HEAD\n1\n=======\n2\n>>>>>>> x\nmiddle\n<<<<<<< HEAD\n=======\n3\n>>>>>>> x\nend"
    got = resolve_conflict(text, "theirs")
    want = "top\n2\nmiddle\n3\nend"
    assert got == want, f"expected {want!r}, got {got!r}"
    assert resolve_conflict("no conflicts here\n", "ours") == "no conflicts here\n", "text without markers is unchanged"


def test_rejects_broken_markers():
    broken = {
        "separator outside a block": "a\n=======\nb\n",
        "end marker outside a block": "a\n>>>>>>> main\n",
        "nested start marker": "<<<<<<< HEAD\n<<<<<<< HEAD\n=======\n>>>>>>> x\n",
        "block with no separator": "<<<<<<< HEAD\na\n>>>>>>> x\n",
        "two separators": "<<<<<<< HEAD\na\n=======\nb\n=======\nc\n>>>>>>> x\n",
        "file ends inside a block": "<<<<<<< HEAD\na\n=======\nb\n",
    }
    for why, text in broken.items():
        assert raises_value_error(text), f"expected ValueError for {why}: {text!r}"


def test_rejects_an_unknown_choice():
    assert raises_value_error(CONFLICTED, "mine"), "choose must be 'ours', 'theirs' or 'both'"
