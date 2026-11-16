def is_palindrome(s: str) -> bool:
    """Return True if s reads the same both ways, ignoring case and non-letters."""
    # TODO: build a lowercase string of only the letters in s ("".join(...) is handy)
    # TODO: compare it with its reverse
    return False


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))   # True
    print(is_palindrome("hello"))                            # False
