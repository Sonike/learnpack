# Dicts and sets

## Why this matters

Lists are great when position matters. But most real questions are about *lookups*: what's the price of this product, how many times has this word appeared, which users are in both groups, have I seen this email before? **Dictionaries** and **sets** answer those questions directly, and they answer them fast, even with millions of items. They're the most-used data structures in Python, and "use a dict" is the answer to a surprising number of interview problems.

## Dictionaries: keys and values

A **dictionary** (`dict`) stores **key → value** pairs. You look things up by key instead of by position:

```python
prices = {"apple": 0.50, "bread": 2.20, "milk": 1.10}
print(prices["bread"])   # 2.2
print(len(prices))       # 3
```

Think of a real dictionary: you look up a word (the key) to find its definition (the value). Keys are unique; values can repeat.

Add or change entries by assigning to a key, and remove them with `del` or `pop`:

```python
prices["eggs"] = 3.00       # add a new key
prices["apple"] = 0.45      # change an existing one
del prices["milk"]          # remove a key
print(prices)               # {'apple': 0.45, 'bread': 2.2, 'eggs': 3.0}
print("bread" in prices)    # True    `in` checks the KEYS
print(2.2 in prices)        # False   values aren't checked
```

Dicts remember the order in which keys were first added, so printing or looping goes in insertion order.

## Missing keys and `get`

Looking up a key that isn't there is an error:

```python
print(prices["cheese"])
# KeyError: 'cheese'
```

When a key might be missing, use `get`, which returns `None`, or a **default** you choose:

```python
print(prices.get("cheese"))        # None
print(prices.get("cheese", 0.0))   # 0.0
print(prices.get("bread", 0.0))    # 2.2
```

## Looping over a dict

```python
stock = {"apple": 12, "bread": 0, "milk": 4}

for name in stock:                  # looping a dict gives its keys
    print(name, end=" ")
# apple bread milk

for name, count in stock.items():   # .items() gives (key, value) pairs
    print(f"{name}: {count}")
# apple: 12
# bread: 0
# milk: 4

print(list(stock.keys()))     # ['apple', 'bread', 'milk']
print(list(stock.values()))   # [12, 0, 4]
```

`for key, value in d.items():` is the one you'll write most. It uses tuple unpacking from "Lists and tuples".

## The counting pattern

"How many times does each thing appear?" is one of the most common jobs in programming. The pattern: for each item, add 1 to its count, starting from 0 if it's new.

```python
votes = ["red", "blue", "red", "green", "red", "blue"]
counts = {}
for colour in votes:
    counts[colour] = counts.get(colour, 0) + 1
print(counts)   # {'red': 3, 'blue': 2, 'green': 1}
```

Read the key line carefully: `counts.get(colour, 0)` is the current count (0 the first time), plus 1, stored back under the same key. This is the accumulator pattern from "Loops", with one accumulator per key.

> **Note:** the standard library has `collections.Counter`, which does this in one line: `Counter(votes)`. Use it in real code once you can write the loop yourself.

## The grouping pattern

Grouping is the counting pattern's sibling: instead of a number per key, you keep a **list** per key.

```python
names = ["Ada", "Alan", "Grace", "Guido", "Linus"]
by_letter = {}
for name in names:
    letter = name[0]
    if letter not in by_letter:
        by_letter[letter] = []        # first time we see this letter: start a list
    by_letter[letter].append(name)
print(by_letter)
# {'A': ['Ada', 'Alan'], 'G': ['Grace', 'Guido'], 'L': ['Linus']}
```

Counting and grouping cover a huge share of everyday data work: totals per customer, orders per day, errors per type.

## Values can be anything

A dict's values can be lists, other dicts, anything. That's how you represent structured records:

```python
user = {
    "name": "Ada",
    "languages": ["Python", "SQL"],
    "address": {"city": "London", "country": "UK"},
}
print(user["languages"][0])         # Python
print(user["address"]["city"])      # London
```

This shape (dicts and lists nested inside each other) is exactly what JSON looks like, the format most web APIs send. You'll meet it again in the web section.

## Sets: unique items, fast membership

A **set** is an unordered collection of **unique** items. Write it with curly brackets, or build it from another collection with `set()`:

```python
tags = {"python", "sql", "python", "git"}
print(tags)          # {'git', 'python', 'sql'}  (duplicates gone; order not guaranteed)
print(len(tags))     # 3
print("sql" in tags) # True

seen = set()         # an empty set ({} on its own is an empty DICT)
seen.add("ada@example.com")
seen.add("ada@example.com")
print(len(seen))     # 1
```

Sets have no order and no indexes: `tags[0]` is a `TypeError`. Use them for two jobs:

1. **Membership:** "have I seen this before?" (`x in seen`).
2. **Removing duplicates:** `set(items)`. But it loses the order. To de-duplicate *and* keep the original order, loop and use a set to remember what you've already kept:

```python
items = [3, 1, 3, 2, 1]
seen = set()
unique = []
for item in items:
    if item not in seen:
        seen.add(item)
        unique.append(item)
print(unique)   # [3, 1, 2]
```

### Set operations

Sets support the operations from maths, with short operators:

```python
alice = {"ben", "cy", "dee"}
bob = {"cy", "dee", "eve"}

print(sorted(alice & bob))   # ['cy', 'dee']                   intersection: in both
print(sorted(alice | bob))   # ['ben', 'cy', 'dee', 'eve']     union: in either
print(sorted(alice - bob))   # ['ben']                         difference: in alice, not bob
print(sorted(alice ^ bob))   # ['ben', 'eve']                  symmetric difference: in exactly one
```

(The examples wrap the result in `sorted()` only so the printed order is predictable. The result of `alice & bob` is itself a set.)

## Why dicts and sets are fast

To check `x in some_list`, Python has to compare `x` with every item until it finds a match. With a million items, that can mean a million comparisons.

Dicts and sets work differently. When you add a key, Python runs it through a **hash function**: a calculation that turns the key into a number, which tells Python where to store it. To look the key up later, Python hashes it again and goes straight to that spot. So `key in my_dict` or `x in my_set` takes roughly the same time with ten items or ten million.

```
list:  "is 'eve' here?"  → check item 0, item 1, item 2, ... (slow when long)
set:   "is 'eve' here?"  → hash('eve') → go straight to its slot (fast)
```

You'll study this properly (it's called a **hash table**) in the data structures section. The practical rule now: **if you're checking membership repeatedly, use a set or a dict, not a list.**

## Hashable keys

Hashing only works if a key can never change. If a key changed after being stored, its hash would change, and Python would look in the wrong place. So dict keys and set items must be **hashable**: in practice, immutable values.

- **Allowed:** `int`, `float`, `str`, `bool`, `None`, and tuples containing only hashable values.
- **Not allowed:** lists, dicts and sets, because they can change.

```python
locations = {(51.5, -0.1): "London"}     # a tuple key: fine
print(locations[(51.5, -0.1)])           # London

bad = {["a", "b"]: 1}
# TypeError: unhashable type: 'list'
```

If you need a list-like key, convert it to a tuple first.

## Common mistakes

**`KeyError`.** You looked up a key that isn't there. The error shows the key, so check its spelling and capitals (`"Apple"` and `"apple"` are different keys), or use `get` with a default.

**Expecting `in` to search values.** `in` on a dict checks keys only. Use `value in d.values()` if you really mean values.

**`{}` for an empty set.** That's an empty dict. Use `set()`.

**Expecting a set to keep order.** Sets are unordered. Sort the result (`sorted(s)`) whenever order matters, such as returning results or printing them in tests.

**`TypeError: unhashable type: 'list'`.** You used a list as a dict key or put one in a set. Use a tuple.

**Changing a dict's size while looping over it.** Adding or deleting keys inside `for k in d:` raises `RuntimeError: dictionary changed size during iteration`. Loop over `list(d)` instead, or build a new dict.

## Recap

- A **dict** maps unique **keys** to values: `d[key]` reads, `d[key] = value` adds or changes, `in` checks keys.
- `d.get(key, default)` avoids `KeyError`. `for key, value in d.items():` loops over pairs.
- **Counting:** `counts[x] = counts.get(x, 0) + 1`. **Grouping:** start an empty list for a new key, then append.
- A **set** holds unique items with no order. Use it for fast membership and de-duplication. `&`, `|`, `-` and `^` are intersection, union, difference and symmetric difference.
- Dict and set lookups are fast because of **hashing**, so keys must be **hashable** (immutable): strings, numbers and tuples, not lists.
