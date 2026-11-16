# Sets: common friends and de-duplication

Two small jobs that sets are made for.

```python
def common_friends(a: set[str], b: set[str]) -> list[str]: ...
def unique_in_order(items: list) -> list: ...
```

- `common_friends(a, b)`: `a` and `b` are two people's sets of friends' names. Return the names in **both** sets as a list sorted A→Z. (Sets have no order, so you sort before returning.)
- `unique_in_order(items)`: return a new list with duplicates removed, keeping the **first** time each item appears, in the original order. Items are hashable (strings, numbers, tuples). `list(set(items))` won't do: it loses the order. Use a set to remember what you've already seen, and a list to build the answer.

## Example

```python
common_friends({"ana", "ben", "cy"}, {"cy", "dee", "ana"})   # ["ana", "cy"]
unique_in_order([3, 1, 3, 2, 1])                               # [3, 1, 2]
unique_in_order(["b", "a", "b"])                               # ["b", "a"]
```
