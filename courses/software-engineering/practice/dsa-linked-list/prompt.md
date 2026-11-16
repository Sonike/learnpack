# A singly linked list

A **linked list** stores each value in its own little object, a **node**, that also points to the next node. The list itself only remembers the first node (the **head**). The `Node` class is written for you.

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next   # the next Node, or None at the end

class LinkedList:
    def __init__(self, values=()): ...
    def append(self, value) -> None: ...
    def prepend(self, value) -> None: ...
    def remove(self, value) -> bool: ...
    def reverse(self) -> None: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
```

- `LinkedList(values)`: start with the given values in order (just `append` each one).
- `append(value)`: add at the end. Keep a `tail` reference so this is O(1).
- `prepend(value)`: add at the front. O(1).
- `remove(value)`: remove the **first** node holding `value` and return `True`, or return `False` if there isn't one. Remember to fix `head` and `tail` when you remove the first or last node.
- `reverse()`: reverse the list **in place** by turning every `next` arrow around. Don't build a new list of values.
- `__iter__`: yield each value from head to tail, so `list(ll)` and `for v in ll` work.
- `__len__`: number of values, O(1) (keep a counter).

## Example

```python
ll = LinkedList([1, 2, 3])
ll.prepend(0)
ll.append(4)
list(ll)        # [0, 1, 2, 3, 4]
ll.remove(2)    # True
ll.reverse()
list(ll)        # [4, 3, 1, 0]
len(ll)         # 4
```
