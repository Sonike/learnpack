from solution import parse_traceback

KEY_ERROR = '''Traceback (most recent call last):
  File "shop.py", line 12, in <module>
    print(total(cart))
  File "shop.py", line 5, in total
    return prices[item] * qty
           ~~~~~~^^^^^^
KeyError: 'banana'
'''


def test_reads_the_innermost_frame():
    got = parse_traceback(KEY_ERROR)
    want = {"type": "KeyError", "message": "'banana'", "file": "shop.py", "line": 5}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_message_can_contain_colons():
    text = '''Traceback (most recent call last):
  File "/home/ada/app/main.py", line 3, in <module>
    int("12:30")
ValueError: invalid literal for int() with base 10: '12:30'
'''
    got = parse_traceback(text)
    want = {"type": "ValueError", "message": "invalid literal for int() with base 10: '12:30'",
            "file": "/home/ada/app/main.py", "line": 3}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_frames_across_files_use_the_last_one():
    text = '''Traceback (most recent call last):
  File "main.py", line 40, in <module>
    report = build_report(rows)
  File "report.py", line 18, in build_report
    avg = average(scores)
  File "stats.py", line 7, in average
    return sum(xs) / len(xs)
           ~~~~~~~~^~~~~~~~~
ZeroDivisionError: division by zero
'''
    got = parse_traceback(text)
    want = {"type": "ZeroDivisionError", "message": "division by zero", "file": "stats.py", "line": 7}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_exception_without_a_message():
    text = '''Traceback (most recent call last):
  File "loop.py", line 2, in <module>
    while True: pass
KeyboardInterrupt

'''
    got = parse_traceback(text)
    want = {"type": "KeyboardInterrupt", "message": "", "file": "loop.py", "line": 2}
    assert got == want, f"expected {want!r}, got {got!r}"


def test_chained_tracebacks_report_the_last_error():
    text = '''Traceback (most recent call last):
  File "config.py", line 9, in load
    data = json.loads(raw)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "app.py", line 4, in <module>
    settings = load()
  File "config.py", line 11, in load
    raise RuntimeError("settings.json is not valid JSON")
RuntimeError: settings.json is not valid JSON
'''
    got = parse_traceback(text)
    want = {"type": "RuntimeError", "message": "settings.json is not valid JSON", "file": "config.py", "line": 11}
    assert got == want, f"expected {want!r}, got {got!r}"
