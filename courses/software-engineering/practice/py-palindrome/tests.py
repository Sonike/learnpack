from solution import is_palindrome


def test_simple_palindromes():
    for s in ["racecar", "level", "a"]:
        got = is_palindrome(s)
        assert got is True, f"is_palindrome({s!r}): expected True, got {got!r}"


def test_not_a_palindrome():
    for s in ["hello", "ab", "palindrome"]:
        got = is_palindrome(s)
        assert got is False, f"is_palindrome({s!r}): expected False, got {got!r}"


def test_ignores_case_spaces_and_punctuation():
    for s in ["A man, a plan, a canal: Panama", "No 'x' in Nixon", "Was it a car or a cat I saw?"]:
        got = is_palindrome(s)
        assert got is True, f"is_palindrome({s!r}): expected True, got {got!r}"


def test_ignores_digits_too():
    got = is_palindrome("ab1ba2")
    assert got is True, f"digits are not letters, so 'ab1ba2' -> 'abba': expected True, got {got!r}"


def test_empty_text_is_a_palindrome():
    for s in ["", "!!", "  "]:
        got = is_palindrome(s)
        assert got is True, f"is_palindrome({s!r}): expected True, got {got!r}"
