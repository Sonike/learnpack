# Hash maps and sets

## Why this matters

If you learn one data structure deeply, make it this one. Python's `dict` and `set` are **hash tables**, and they turn "search the whole list" (O(n)) into "jump straight to it" (O(1) on average). That single trick is the answer to a huge number of interview questions and everyday performance bugs. Caches, database indexes, de-duplication, counting and "have I seen this before?" all run on it.

## 1. The idea: compute where things go

Imagine a cloakroom with 8 numbered hooks. Instead of hanging coats anywhere and searching every hook later, you use a rule that turns a person's name into a hook number. To fetch a coat, apply the rule again and go straight to that hook.

In code, the rule is a **hash function**: it turns a value into an integer, called its **hash**. Python's built-in `hash()` does it:

```python
print(hash(42))        # 42          small ints hash to themselves
print(hash("apple"))   # e.g. -2382150936893218340  (a big integer)
print(hash("apple") == hash("apple"))  # True      same value, same hash
```

> **Note:** String hashes change every time you start Python (a security feature called hash randomisation), so your number will differ from the one above. Within one run, the same string always gives the same hash.

A hash table keeps a list of **buckets**. To find the bucket for a key, take the hash modulo (`%`, the remainder after division) the number of buckets:

```python
buckets = 8
for key in ["apple", "pear", "fig"]:
    print(key, hash(key) % buckets)
# apple 3
# pear 6
# fig 3      (your numbers will differ)
```

Putting a value in: compute the bucket, store `(key, value)` there. Getting it back: compute the same bucket, look there. Computing a hash and a `%` takes the same time whether the table holds 10 items or 10 million, which is why lookups are O(1).

## 2. Collisions and chaining

In the output above, `"apple"` and `"fig"` landed in the same bucket. That's a **collision**, and it's unavoidable: there are endless possible keys and only so many buckets.

The simplest fix is **chaining**: each bucket holds a small list of `(key, value)` pairs. To look up a key, go to its bucket and check the few pairs there with `==`.

```
bucket 0: []
bucket 1: []
bucket 2: []
bucket 3: [("apple", 3), ("fig", 8)]     <- collision: both live here
bucket 4: []
bucket 5: []
bucket 6: [("pear", 5)]
bucket 7: []
```

Here is a tiny lookup in that style:

```python
buckets = [[] for _ in range(8)]

def put(key, value):
    bucket = buckets[hash(key) % len(buckets)]
    for pair in bucket:
        if pair[0] == key:      # already there: replace
            pair[1] = value
            return
    bucket.append([key, value])

def get(key):
    for k, v in buckets[hash(key) % len(buckets)]:
        if k == key:
            return v
    return None

put("apple", 3)
put("apple", 4)
print(get("apple"), get("kiwi"))  # 4 None
```

(Python's real `dict` uses a different collision strategy called open addressing, but the costs work out the same way and chaining is easier to picture.)

## 3. Load factor and resizing

Lookups are fast only while buckets stay short. The **load factor** is:

```
load factor = number of keys / number of buckets
```

With 8 buckets and 6 keys, it's 0.75: on average each bucket holds less than one key. If you kept adding keys without adding buckets, chains would grow and lookups would slide toward O(n).

So hash tables **resize**: when the load factor passes a threshold (0.75 is a common choice), make a table with twice as many buckets and re-insert every key. Every key's bucket number changes, because the `%` is now by a different number. A resize is O(n), but like a list's growth it happens rarely enough (each time the size doubles) that inserting stays **O(1) amortised**.

You'll build exactly this in the "Build your own hash map" exercise: chaining, a 0.75 load factor, and doubling.

## 4. Why "O(1) on average" and not always

Everything above assumes the hash function spreads keys out evenly. What if every key landed in the **same** bucket?

```python
class BadKey:
    def __init__(self, name):
        self.name = name
    def __hash__(self):
        return 42                     # every BadKey collides
    def __eq__(self, other):
        return self.name == other.name

table = {BadKey(str(i)): i for i in range(2000)}  # works, but slowly
```

Then one bucket holds every key, a lookup has to compare against each one with `==`, and you're back to a list: **O(n) per lookup, worst case**. Good hash functions (like Python's built-in ones) make this vanishingly unlikely for normal data, so in practice we say dict and set operations are **O(1) on average, O(n) worst case**.

## 5. Hashable and unhashable

For this to work, a key's hash must **never change** while it's in the table. If it did, you'd look in the wrong bucket and never find it again.

That's why only **immutable** values can be keys. Python calls them **hashable**:

```
Hashable (can be a key or set member)     Unhashable
int, float, str, bool, None               list
tuple (if everything inside is hashable)   dict
frozenset                                  set
```

```python
locations = {(51.5, -0.1): "London"}   # a tuple key: fine
print(locations[(51.5, -0.1)])         # London

bad = {[1, 2]: "nope"}
# TypeError: unhashable type: 'list'
```

(Python 3.14 words it as `cannot use 'list' as a dict key (unhashable type: 'list')`.) When you see `unhashable type: 'list'`, you used a list as a dict key or put it in a set. The usual fix is to convert it to a tuple: `tuple(my_list)`.

## 6. dict and set in Python

A **dict** maps keys to values. A **set** is the same machinery with keys only: it stores unique values and answers "is this in here?" in O(1) on average.

```python
stock = {"apple": 3}
stock["pear"] = 5               # insert: O(1) avg
print(stock.get("kiwi", 0))     # 0          missing key with a default
print("pear" in stock)          # True       O(1) avg
del stock["apple"]              # delete: O(1) avg

seen = set()
seen.add("ada")
print("ada" in seen, "bob" in seen)  # True False
print(set([3, 1, 3, 2, 1]))          # {1, 2, 3}   duplicates removed
```

Two helpers from `collections` save a lot of code:

```python
from collections import Counter, defaultdict

print(Counter("banana"))         # Counter({'a': 3, 'n': 2, 'b': 1})

by_length = defaultdict(list)    # missing keys start as []
for word in ["hi", "cat", "to", "dog"]:
    by_length[len(word)].append(word)
print(dict(by_length))           # {2: ['hi', 'to'], 3: ['cat', 'dog']}
```

> **Note:** Since Python 3.7, dicts remember the order keys were inserted. Sets do **not** promise any order; don't rely on the printed order of a set.

## 7. Three interview patterns

Most "use a hash map" problems are one of three shapes.

**Seen-before.** Walk the input once, remembering what you've passed. The classic is **two sum** on an *unsorted* list (two pointers needs sorting; this doesn't):

```python
def two_sum(nums, target):
    index_of = {}                       # value -> index
    for j, number in enumerate(nums):
        partner = target - number
        if partner in index_of:         # O(1) avg
            return (index_of[partner], j)
        index_of[number] = j
    return None

print(two_sum([2, 7, 11, 15], 9))  # (0, 1)
```

O(n) time, O(n) space: the trade from the lesson "Big-O from zero", memory for speed.

**Group by key.** Compute a key for each item and collect items with the same key. Anagrams (words with the same letters) share their sorted letters:

```python
groups = {}
for word in ["eat", "tea", "tan", "ate", "nat"]:
    key = "".join(sorted(word))         # "aet" for eat/tea/ate
    groups.setdefault(key, []).append(word)
print(list(groups.values()))  # [['eat', 'tea', 'ate'], ['tan', 'nat']]
```

**Count.** "Most common", "appears exactly once", "is this a permutation of that": count with a `Counter`, then answer from the counts.

```python
from collections import Counter

def first_unique_char(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1

print(first_unique_char("loveleetcode"))  # 2   ('v')
```

Whenever a brute force has "for each item, search the list for…", ask whether a dict or set could answer that search in O(1).

## Common mistakes

**`KeyError: 'kiwi'`.** You read `d["kiwi"]` and the key isn't there. Use `d.get("kiwi")` (returns `None`) or `d.get("kiwi", 0)`, check `"kiwi" in d` first, or use a `defaultdict`/`Counter`.

**`TypeError: unhashable type: 'list'`.** A list as a key or set member. Use a tuple.

**Changing a dict while looping over it.** `for k in d: del d[k]` raises `RuntimeError: dictionary changed size during iteration`. Loop over a copy: `for k in list(d):`.

**Building the set inside the loop.** `if x in set(other_list):` inside a loop rebuilds the set (O(n)) every time. Build it once, before the loop.

**Expecting order from a set.** If you need sorted output, call `sorted()` on it.

**Thinking a dict is free.** It's O(1) *time*, but it uses O(n) *memory*, and a dict of millions of entries takes real RAM. Usually worth it; say so in an interview.

## Recap

- A hash function turns a key into an integer; `hash % buckets` picks the bucket. That's why dict and set lookups are O(1) on average.
- Collisions are normal; **chaining** keeps colliding pairs in a short list per bucket.
- Tables resize when the **load factor** passes a threshold, keeping chains short; inserts stay O(1) amortised.
- If everything collides, lookups degrade to O(n): that's the worst case.
- Only hashable (immutable) values can be keys; use tuples instead of lists.
- Three patterns cover most problems: **seen-before**, **group by key**, **count**.
