from solution import make_greeting


def test_informal_by_default():
    got = make_greeting("Sam")
    assert got == "Hi, Sam!", f"expected 'Hi, Sam!', got {got!r}"


def test_formal_greeting():
    got = make_greeting("Sam", formal=True)
    assert got == "Good day, Sam.", f"expected 'Good day, Sam.', got {got!r}"


def test_title_goes_before_the_name():
    got = make_greeting("Okafor", formal=True, title="Dr")
    assert got == "Good day, Dr Okafor.", f"expected 'Good day, Dr Okafor.', got {got!r}"
    got = make_greeting("Sam", title="Captain")
    assert got == "Hi, Captain Sam!", f"expected 'Hi, Captain Sam!', got {got!r}"


def test_formal_must_be_passed_by_name():
    try:
        got = make_greeting("Sam", True)
    except TypeError:
        return
    assert False, f"make_greeting('Sam', True) should raise TypeError (keyword-only), but returned {got!r}"


def test_title_must_be_passed_by_name():
    try:
        got = make_greeting("Sam", False, "Dr")
    except TypeError:
        return
    assert False, f"make_greeting('Sam', False, 'Dr') should raise TypeError, but returned {got!r}"
