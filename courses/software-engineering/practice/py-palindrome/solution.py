def is_palindrome(s: str) -> bool:
    """Return True if s reads the same both ways, ignoring case and non-letters."""
    letters = "".join(ch.lower() for ch in s if ch.isalpha())
    return letters == letters[::-1]


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))   # True
    print(is_palindrome("hello"))                            # False
