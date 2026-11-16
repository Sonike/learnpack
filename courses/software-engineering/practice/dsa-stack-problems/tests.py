from solution import eval_rpn, is_balanced


def test_balanced_text():
    for text in ["print(items[0])", "{[()]}", "", "no brackets here", "()[]{}"]:
        got = is_balanced(text)
        assert got is True, f"is_balanced({text!r}): expected True, got {got!r}"


def test_unbalanced_text():
    for text in ["([)]", "((", ")", "(]", "{[}"]:
        got = is_balanced(text)
        assert got is False, f"is_balanced({text!r}): expected False, got {got!r}"


def test_eval_rpn_basic_operations():
    for tokens, want in [(["3", "4", "+"], 7), (["10", "3", "-"], 7), (["6", "7", "*"], 42), (["8", "2", "/"], 4)]:
        got = eval_rpn(tokens)
        assert got == want, f"eval_rpn({tokens!r}): expected {want}, got {got!r}"


def test_eval_rpn_chains_operations():
    tokens = ["4", "13", "5", "/", "+"]  # 4 + (13 / 5) = 4 + 2
    got = eval_rpn(tokens)
    assert got == 6, f"expected 6, got {got!r}"
    got = eval_rpn(["2", "3", "+", "4", "*"])
    assert got == 20, f"expected 20, got {got!r}"


def test_eval_rpn_division_truncates_toward_zero():
    got = eval_rpn(["-7", "2", "/"])
    assert got == -3, f"expected -3, got {got!r}"


def test_eval_rpn_single_number():
    got = eval_rpn(["-5"])
    assert got == -5, f"expected -5, got {got!r}"
