# Stacks, queues and linked lists

## Why this matters

Your editor's undo button is a stack. A web server's waiting requests are a queue. The browser's back button is a stack; a printer's jobs are a queue. These two simple structures, defined by *which end you add and remove from*, show up everywhere in real systems and in interviews. **Linked lists** matter less in everyday Python, but they're an interview favourite because they test whether you can reason about references (pointers) without getting lost.

## 1. Stacks: last in, first out

A **stack** is a pile: you can only add to the top (**push**) and take from the top (**pop**). The last thing in is the first thing out, which is called **LIFO**.

```
push 1     push 2     push 3     pop -> 3   pop -> 2
                      | 3 |
           | 2 |      | 2 |      | 2 |
| 1 |      | 1 |      | 1 |      | 1 |      | 1 |
+---+      +---+      +---+      +---+      +---+
```

A Python list is a perfect stack, because adding and removing at the **end** is O(1):

```python
stack = []
stack.append("type 'h'")     # push
stack.append("type 'i'")
stack.append("bold")
print(stack[-1])             # bold        peek at the top without removing
print(stack.pop())           # bold        undo the last action
print(stack.pop())           # type 'i'
print(len(stack))            # 1
```

Use a stack whenever the most recent thing is the one you need next: undo history, the browser back button, the call stack from the lesson "Recursion and binary search", and depth-first search in the next lesson.

**Example: balanced brackets.** Is every `(`, `[` and `{` in some code closed by its partner, in the right order? Each closing bracket must match the **most recent** unmatched opening one, which is exactly the top of a stack.

```python
PAIRS = {")": "(", "]": "[", "}": "{"}

def is_balanced(text):
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in PAIRS:
            if not stack or stack[-1] != PAIRS[ch]:
                return False         # nothing to close, or the wrong partner
            stack.pop()
    return not stack                 # anything left open is unbalanced

print(is_balanced("print(items[0])"))  # True
print(is_balanced("([)]"))             # False
print(is_balanced("(("))               # False
```

Trace `"([)]"`: push `(`, push `[`, then `)` arrives but the top is `[`: mismatch, `False`. One pass, O(n) time, O(n) space in the worst case.

**Example: reverse Polish notation.** In RPN the operator comes after its numbers: `3 4 +` means `3 + 4`, and `2 3 + 4 *` means `(2 + 3) * 4`. Calculators and compilers like it because it never needs brackets. Evaluate it with a stack: push numbers; on an operator, pop two numbers, combine them and push the result.

```
tokens:  2   3   +   4   *
stack:  [2] [2,3] [5] [5,4] [20]
```

You'll write this one in the "Two stack problems" exercise.

## 2. Queues: first in, first out

A **queue** is a line at a shop: join at the back (**enqueue**), leave from the front (**dequeue**). First in, first out: **FIFO**.

```
enqueue A, B, C:      front -> [A, B, C] <- back
dequeue -> A:         front -> [B, C]    <- back
enqueue D:            front -> [B, C, D] <- back
```

Queues keep things fair and in order: print jobs, requests waiting for a server, messages waiting to be processed, and breadth-first search in the next lesson.

**Don't use a list as a queue.** Taking from the front of a list is `list.pop(0)`, and as you saw in the lesson "Arrays, two pointers and sliding windows", that shifts every remaining item: O(n). In a loop that empties a queue of `n` items, that's O(n²).

Use `collections.deque` (pronounced "deck", short for **double-ended queue**). It's O(1) at **both** ends:

```python
from collections import deque

jobs = deque()
jobs.append("report.pdf")       # enqueue at the back
jobs.append("photo.png")
jobs.append("invoice.pdf")
print(jobs.popleft())           # report.pdf    dequeue from the front: O(1)
print(jobs[0])                  # photo.png     peek at the front
print(len(jobs))                # 2
```

A deque can also be built with a maximum length, which quietly drops the oldest item when a new one arrives: handy for "the last 100 log lines".

```python
recent = deque(maxlen=3)
for line in ["a", "b", "c", "d"]:
    recent.append(line)
print(list(recent))   # ['b', 'c', 'd']
```

**Example: counting recent requests.** A rate limiter asks "how many requests in the last `window` seconds?" Keep their timestamps in a deque: add each new one at the back, and drop old ones from the front until the front is recent enough.

```python
from collections import deque

class RecentCounter:
    def __init__(self, window):
        self.window = window
        self.times = deque()

    def ping(self, t):
        self.times.append(t)
        while self.times[0] < t - self.window:
            self.times.popleft()
        return len(self.times)

c = RecentCounter(3000)
print([c.ping(t) for t in [1, 100, 3001, 3002]])  # [1, 2, 3, 3]
```

Notice `ping` takes the time `t` as an argument instead of reading the clock. That makes it easy to test with exact numbers, which you'll do in the exercise. Each timestamp is added once and removed at most once, so `ping` costs O(1) on average.

## 3. Linked lists: nodes and references

A Python list keeps its items side by side in one block of memory. A **linked list** does the opposite: each item lives in its own small object, called a **node**, and each node holds a reference to the **next** node. The list only needs to remember the first node, the **head**.

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next      # the next Node, or None at the end
```

```
head
 |
 v
+-------+---+     +-------+---+     +-------+------+
|   1   | o-----> |   2   | o-----> |   3   | None |
+-------+---+     +-------+---+     +-------+------+
  value  next
```

Building and walking one:

```python
head = Node(1, Node(2, Node(3)))

current = head
while current is not None:     # follow the arrows until there are none
    print(current.value)
    current = current.next
# 1
# 2
# 3
```

The trade-offs are the mirror image of a Python list's:

```
                               Python list    Linked list
get item i                     O(1)           O(n)  must walk from head
add/remove at the front        O(n)           O(1)  just move head
add at the end                 O(1)*          O(1)  if you keep a tail reference
remove a node you already hold O(n)           O(1)  re-point one arrow
memory per item                small          bigger (each node is an object)
```

**Adding at the front** creates a node pointing at the old head, then moves `head`:

```
before:   head -> [1] -> [2] -> None
new node: [0] -> [1]
after:    head -> [0] -> [1] -> [2] -> None
```

**Removing** a node means making the node *before* it skip over it:

```
remove 2:   [1] -> [2] -> [3]
                becomes
            [1] ---------> [3]        (nothing points at [2] any more; Python frees it)
```

So you walk the list with **two** references, `prev` and `current`, so that when `current` is the one to remove, you can set `prev.next = current.next`. If the node to remove is the head (there's no `prev`), move `head` instead.

**Reversing** is the classic interview question. Walk once, turning each arrow around. You need three references, because the moment you flip `current.next`, you'd lose the rest of the list unless you saved it first:

```python
def reverse(head):
    prev = None
    current = head
    while current is not None:
        next_node = current.next   # 1. save the rest of the list
        current.next = prev        # 2. flip this arrow
        prev = current             # 3. step forward
        current = next_node
    return prev                    # the old tail is the new head

head = reverse(Node(1, Node(2, Node(3))))
print(head.value, head.next.value, head.next.next.value)  # 3 2 1
```

```
start:    None    [1] -> [2] -> [3] -> None
          prev    cur
step 1:   None <- [1]    [2] -> [3] -> None
                  prev   cur
step 2:   None <- [1] <- [2]    [3] -> None
                         prev   cur
step 3:   None <- [1] <- [2] <- [3]    None
                                prev   cur    -> return prev
```

Drawing boxes and arrows on paper like this is the single best habit for linked-list problems, at a desk or in an interview.

**When do linked lists matter in Python?** Rarely directly: `list` and `deque` cover almost every need (a deque is built from linked blocks internally). They matter for understanding how structures are built from references, for trees and graphs (which are linked structures with more than one arrow per node), and for interviews. In the "A singly linked list" exercise you'll build one with `append`, `prepend`, `remove`, `reverse`, `__iter__` and `__len__`.

## 4. Choosing between them

```
You need...                                   Use
the most recent item next (undo, back, DFS)   stack: list with append/pop
the oldest item next (fair order, BFS)        queue: collections.deque
fast access by position                       list
cheap insert/remove at both ends              deque
a "last N items" buffer                       deque(maxlen=N)
```

## Common mistakes

**`IndexError: pop from empty list`** (or `pop from an empty deque`). You popped when there was nothing left, often a closing bracket with no opener. Check `if stack:` before popping, as `is_balanced` does.

**Using `list.pop(0)` as a queue.** It works, so nothing warns you, but it's O(n) per call. On a big queue the program crawls. Use `deque.popleft()`.

**`AttributeError: 'NoneType' object has no attribute 'next'`.** You walked off the end of a linked list: `current` became `None` and you still read `current.next`. Loop `while current is not None`, and check before reaching two steps ahead (`current.next.next`).

**Losing the rest of the list.** Setting `current.next = prev` *before* saving `current.next` cuts the list in two, and everything after is gone. Save first, then flip.

**Forgetting the head and tail.** Removing the first node must move `head`; removing the last must move `tail` if you keep one. Test removing the first item, the last item and the only item.

## Recap

- **Stack:** LIFO; a Python list with `append` and `pop`, both O(1). Use it for "most recent first": undo, back buttons, bracket matching, DFS.
- **Queue:** FIFO; use `collections.deque` with `append` and `popleft`, both O(1). Never `list.pop(0)`.
- **Linked list:** nodes holding a value and a reference to the next node. O(1) at the head, O(n) to reach position i.
- Draw boxes and arrows; for removal keep `prev`, for reversal save `next` before flipping.
