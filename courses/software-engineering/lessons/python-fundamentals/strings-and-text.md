# Strings and text

## Why this matters

A huge share of programming is text handling: cleaning what users type into forms, reading CSV and log files, building messages and reports, checking that an email address looks plausible. Python's string tools are excellent, and knowing them well turns twenty-line loops into one clear line. This lesson also introduces **regular expressions**, a small pattern language you'll find in every editor, every language and every codebase.

## Strings are sequences

A string is a **sequence of characters**, so everything you learned about indexing and slicing lists works on strings too:

```python
word = "Python"
print(len(word))     # 6
print(word[0])       # P
print(word[-1])      # n
print(word[1:4])     # yth
print(word[::-1])    # nohtyP     reversed
print("th" in word)  # True       substring check
for ch in "hi!":
    print(ch, end=" ")
# h i !
```

## Strings are immutable

Unlike lists, strings can't be changed in place. Every string method returns a **new** string and leaves the original alone:

```python
name = "ada"
name.upper()
print(name)              # ada     unchanged: the result was thrown away
name = name.upper()      # keep the result by assigning it
print(name)              # ADA

name[0] = "E"
# TypeError: 'str' object does not support item assignment
```

To "change" a string, build a new one: `"E" + name[1:]`. Immutability is also why strings can be dict keys (they're hashable, from "Dicts and sets").

## The methods you'll use every day

### Cleaning

```python
raw = "   Hello, World!  \n"
print(repr(raw.strip()))    # 'Hello, World!'    remove whitespace from both ends
print(repr(raw.lstrip()))   # 'Hello, World!  \n'   left side only
print("--hi--".strip("-"))  # hi                 strip specific characters
```

`repr()` shows a string with its quotes and any invisible characters such as `\n` (a new line), which is very useful when debugging text. `.strip()` is the first thing to do with anything a user typed or a line read from a file.

### Case

```python
s = "hello World"
print(s.lower())        # hello world
print(s.upper())        # HELLO WORLD
print(s.title())        # Hello World      every word capitalised
print(s.capitalize())   # Hello world      only the first character
```

To compare text ignoring case, lowercase both sides: `answer.lower() == "yes"`.

### Searching and testing

```python
filename = "report-2026.csv"
print(filename.startswith("report"))   # True
print(filename.endswith(".csv"))       # True
print(filename.find("2026"))           # 7     index where it starts
print(filename.find("2027"))           # -1    not found
print(filename.count("r"))             # 2
print("2026".isdigit(), "abc".isalpha(), "abc1".isalnum())   # True True True
```

`find` returns `-1` when there's no match. Its cousin `index` raises a `ValueError` instead.

### Replacing

```python
print("Hello".replace("l", "L"))            # HeLLo
print("a-b-c".replace("-", " ", 1))         # a b-c   only the first occurrence
```

## `split` and `join`

These two are opposites, and together they're the workhorses of text processing.

`split` breaks a string into a **list** of pieces:

```python
print("2026-11-13".split("-"))     # ['2026', '11', '13']
print("a,b,,c".split(","))         # ['a', 'b', '', 'c']   empty piece between the two commas
print("  too   many spaces ".split())   # ['too', 'many', 'spaces']
```

Note the difference: with a separator, `split(",")` keeps empty pieces. With **no argument**, `split()` splits on any run of whitespace and drops empty pieces, which is nearly always what you want for words.

`join` goes the other way. It's called on the **separator** and takes a list of strings:

```python
words = ["the", "quick", "fox"]
print(" ".join(words))    # the quick fox
print(", ".join(words))   # the, quick, fox
print("".join(["a", "b", "c"]))   # abc
```

`join` only accepts strings: `", ".join([1, 2])` raises `TypeError: sequence item 0: expected str instance, int found`. Convert first: `", ".join(str(n) for n in nums)`.

### Building strings efficiently

If you build a long string by adding pieces in a loop with `+=`, Python may create a new string for every addition, because strings are immutable. For a few pieces it doesn't matter. For thousands, collect the pieces in a list and `join` once at the end:

```python
parts = []
for n in range(5):
    parts.append(f"item{n}")
print(", ".join(parts))   # item0, item1, item2, item3, item4
```

The pattern "transform each piece, then join" also handles a lot of cleaning in one line:

```python
messy = "  hELLo   wORLD "
print(" ".join(w.capitalize() for w in messy.split()))   # Hello World
```

That expression in the brackets, `w.capitalize() for w in messy.split()`, is a **generator expression**: a compact loop that produces one value per item. You'll see it often. Read it as "capitalize `w`, for each `w` in the split words".

## Formatting with f-strings

You've used f-strings since "Values, variables and types". A few more format specs worth knowing:

```python
name, score, ratio = "Ada", 7, 0.257
print(f"{name:>6}|")       #    Ada|    right-align in 6 characters
print(f"{name:<6}|")       # Ada   |    left-align
print(f"{name:^7}|")       #   Ada  |   centre
print(f"{score:03d}")      # 007        pad with zeros
print(f"{ratio:.1%}")      # 25.7%      as a percentage
print(f"{1234567.891:,.2f}")   # 1,234,567.89
print(f"{name=}")          # name='Ada'   handy for debugging
```

Alignment is how you print tidy tables in the terminal.

## Regular expressions: a light introduction

Sometimes you need to match a *pattern*, not a fixed string: "any run of digits", "something that looks like a phone number". A **regular expression** (regex) is a mini-language for describing patterns. Python's `re` module runs them.

A few building blocks:

```
\d       any digit 0-9              .        any character (except new line)
\s       any whitespace             [abc]    one of a, b or c
\w       a letter, digit or _       [^@]     any character EXCEPT @
+        one or more of the previous         {2,}   two or more of the previous
*        zero or more                        ?      optional (zero or one)
```

Always write patterns as **raw strings**, `r"..."`, so Python passes the backslashes through to `re` unchanged.

```python
import re

text = "Order 66 shipped 3 items"
print(re.findall(r"\d+", text))        # ['66', '3']        every match
print(re.search(r"\d+", text).group()) # 66                 the first match
print(re.sub(r"\s+", " ", "too    many   spaces"))   # too many spaces

print(bool(re.fullmatch(r"\d{3}-\d{4}", "555-1234")))    # True
print(bool(re.fullmatch(r"\d{3}-\d{4}", "555-12345")))   # False
```

- `re.search` finds the first match **anywhere** in the text (or returns `None`).
- `re.fullmatch` succeeds only if the **whole** string matches, which is what you want for validation.
- `re.findall` returns a list of all matches.
- `re.sub` replaces every match.

### A simple email check

This lesson's last exercise checks whether text *looks like* an email address with a deliberately loose pattern:

```
[^@\s]+   @   [^@\s]+   \.   [A-Za-z]{2,}
 local   one   domain   dot   2+ letters at the end
 part     @
```

It accepts `ada@example.com` and rejects `ada.example.com` and `ada@example`. Real email addresses are allowed to be far stranger than this, and a pattern that tries to cover the full rules is unreadable. That's why real systems use a simple check to catch typos and then **send a confirmation email**: the only reliable test of an address is whether its owner receives the message.

Regex is powerful and easy to overdo. If `startswith`, `in`, `split` or `isdigit` can do the job, use them; they're clearer. Reach for `re` when the pattern genuinely varies. The Python Regular Expression HOWTO (linked below) is the guide to read when you need more.

## Common mistakes

**Calling a method and forgetting to keep the result.** `name.strip()` on its own line does nothing useful. Write `name = name.strip()`.

**Trying to change a character in place.** `s[0] = "x"` raises `TypeError: 'str' object does not support item assignment`. Build a new string.

**`split(",")` vs `split()`.** The first keeps empty pieces (`"a,,b"` gives `['a', '', 'b']`); the second splits on any whitespace and drops empties.

**`join` with non-strings.** `TypeError: sequence item 0: expected str instance, int found`. Convert each item with `str()` first.

**Forgetting the `r` on a regex.** Without it, `"\b"` becomes a backspace character before `re` ever sees it, and your pattern silently matches nothing. Use `r"..."` every time.

**Using `re.search` for validation.** `re.search(r"\d+", "abc123xyz")` finds a match, so "contains digits" passes even with letters around them. Use `re.fullmatch` when the whole string must fit.

**Comparing text without normalising it.** `"Yes " == "yes"` is `False`. Strip and lowercase first.

## Recap

- Strings are **immutable sequences**: index, slice and loop like lists, but methods return **new** strings.
- Everyday methods: `strip`, `lower`/`upper`/`title`/`capitalize`, `startswith`/`endswith`, `find`, `count`, `replace`, `isdigit`/`isalpha`.
- `split` turns a string into a list; `"sep".join(list)` turns a list of strings back into one string. Build big strings with a list and one `join`.
- f-string format specs handle alignment (`:>6`), padding (`:03d`), decimals (`:.2f`) and percentages (`:.1%`).
- `re` matches patterns: `search`, `fullmatch`, `findall`, `sub`. Use raw strings, prefer plain string methods when they suffice, and remember that real email validation means sending an email.
