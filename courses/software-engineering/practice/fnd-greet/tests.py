from solution import greet


def test_greets_a_simple_name():
    got = greet("Ada")
    assert got == "Hello, Ada!", f"expected 'Hello, Ada!', got {got!r}"


def test_capitalises_the_name():
    got = greet("ada")
    assert got == "Hello, Ada!", f"expected 'Hello, Ada!', got {got!r}"


def test_strips_spaces_and_fixes_capitals():
    got = greet("  grace HOPPER ")
    assert got == "Hello, Grace Hopper!", f"expected 'Hello, Grace Hopper!', got {got!r}"


def test_blank_name_greets_a_stranger():
    for name in ["", "   "]:
        got = greet(name)
        assert got == "Hello, stranger!", f"greet({name!r}): expected 'Hello, stranger!', got {got!r}"
