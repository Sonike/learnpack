from solution import add


def test_stage_1_empty_one_and_two_numbers():
    for text, want in [("", 0), ("4", 4), ("1,2", 3)]:
        got = add(text)
        assert got == want, f"add({text!r}): expected {want!r}, got {got!r}"


def test_stage_2_any_amount_of_numbers():
    got = add("1,2,3,4,5")
    assert got == 15, f"expected 15, got {got!r}"


def test_stage_3_newlines_are_separators():
    for text, want in [("1\n2,3", 6), ("1\n2\n3", 6)]:
        got = add(text)
        assert got == want, f"add({text!r}): expected {want!r}, got {got!r}"


def test_stage_4_custom_delimiter():
    for text, want in [("//;\n1;2", 3), ("//|\n1|2,3", 6), ("//;\n5", 5)]:
        got = add(text)
        assert got == want, f"add({text!r}): expected {want!r}, got {got!r}"


def test_stage_5_negatives_are_all_listed():
    try:
        add("1,-2,3,-4")
    except ValueError as e:
        got = str(e)
        assert got == "negatives not allowed: -2, -4", f"expected 'negatives not allowed: -2, -4', got {got!r}"
        return
    raise AssertionError("add('1,-2,3,-4') should raise ValueError")
