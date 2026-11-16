# The bakery stock kata: add a feature to tangled code

A small bakery tracks how fresh its stock is. Every night, `update_inventory(items)` ages each item by one day. The code works, but it's a knot of nested `if`s, and the owner wants a new kind of item. This is a **kata** (a practice exercise you can repeat) in the style of the famous "Gilded Rose".

Each `Item` has a `name`, `sell_in` (days left before its best-before date) and `quality` (0 to 50). The current rules:

- At the end of each day, `sell_in` goes down by 1 and `quality` goes down by 1.
- Once the best-before date has passed (`sell_in` is below 0 after the update), quality drops **twice** as fast (by 2).
- Quality is never negative.
- **`"Aged Cheese"`** gets *better* with age: quality goes **up** by 1 (by 2 once past its date). Quality never goes above 50.
- **`"Honey"`** never spoils: neither its `sell_in` nor its `quality` ever change.

**The new rule:** `"Fresh Bread"` goes stale twice as fast as normal items: quality drops by 2 per day, and by 4 once past its date (still never below 0).

```python
class Item:                      # given; don't change it
    def __init__(self, name: str, sell_in: int, quality: int): ...

def update_inventory(items: list[Item]) -> None: ...   # changes the items in place
```

## How to work

1. **Pin down today's behaviour first.** Before touching the code, write a few `assert`s in the `__main__` block for the existing rules (a normal item, a past-date item, cheese at 50, honey). These are **characterization tests**: they record what the code does now, so you'll know if you break it.
2. Refactor until adding a rule is easy. One clear branch per item type beats nested `if name != ...`.
3. Add the Fresh Bread rule.

The hidden tests check every old rule plus the new one.

## Example

```python
items = [Item("Croissant", 1, 10), Item("Fresh Bread", 0, 5), Item("Aged Cheese", 3, 49)]
update_inventory(items)
[(i.sell_in, i.quality) for i in items]   # [(0, 9), (-1, 1), (2, 50)]
```
