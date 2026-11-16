def parse_traceback(text: str) -> dict:
    """Return {"type", "message", "file", "line"} for the innermost frame of a traceback."""
    lines = text.strip().splitlines()
    # TODO: the last line holds "Type: message" (the message may be missing)
    # TODO: find the last line that starts with 'File "' (after stripping spaces)
    # TODO: pull the file name out of the quotes and the number after "line "
    return {"type": "", "message": "", "file": "", "line": 0}


if __name__ == "__main__":
    example = '''Traceback (most recent call last):
  File "shop.py", line 12, in <module>
    print(total(cart))
  File "shop.py", line 5, in total
    return prices[item] * qty
KeyError: 'banana'
'''
    print(parse_traceback(example))
    # want: {'type': 'KeyError', 'message': "'banana'", 'file': 'shop.py', 'line': 5}
