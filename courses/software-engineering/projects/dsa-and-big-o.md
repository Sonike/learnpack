# DSA notebook: your interview toolkit

Build a repository of your own hand-written, tested data structures and algorithms, with notes in your own words. It's the thing you'll revise from the night before every technical interview, and it doubles as proof that you understand what's underneath `dict`, `sorted` and `deque` rather than just calling them.

Plan on two to three weeks of evenings: about a week for the implementations, and the rest spread out over the 30 practice problems.

## What you're building

A GitHub repository laid out something like this:

```
dsa-notebook/
├── README.md              index: every structure, its Big-O table and when to use it
├── dsa/
│   ├── hash_map.py
│   ├── linked_list.py
│   ├── stack_queue.py
│   ├── bst.py
│   ├── graph_search.py    BFS and DFS
│   ├── merge_sort.py
│   └── binary_search.py
├── tests/
│   └── test_*.py          one test file per module, run with pytest
├── problems/
│   └── 001-two-sum.md     one note per practice problem
├── bench.py
├── RESULTS.md             your benchmark table
└── MISTAKES.md            your mistakes log
```

The exact layout is yours. What matters is that someone (you, in three months, or a reviewer) can find any structure in a few seconds.

## Requirements

### 1. Hand-written implementations, all tested

Write each of these yourself, without copying from the lessons. Rewriting from memory is the point: it's what an interview asks of you.

- **Hash map** with chaining and resizing (`put`, `get`, `remove`, `__len__`), no `dict` inside.
- **Linked list** (`append`, `prepend`, `remove`, `reverse`, `__iter__`, `__len__`).
- **Stack and queue.** The stack can wrap a list; build the queue on `collections.deque` and write one sentence on why not `list.pop(0)`.
- **Binary search tree** with `insert`, `contains` and an in-order traversal, plus an `is_valid_bst` check.
- **BFS and DFS** on an adjacency-list graph: BFS returning shortest distances, DFS returning connected components.
- **Merge sort**, stable, returning a new list.
- **Binary search** and **lower bound**.

Each module has tests covering normal cases and edge cases: empty input, one item, duplicates, the item at either end, not found. Compare against the built-in where one exists (`sorted`, `bisect.bisect_left`, `dict`) on random inputs generated from a fixed seed, as the practice exercises did.

### 2. A Big-O table and "when to use" for each

At the top of each module (or in the README), a small table with the time and space cost of every operation, and one line on when you'd reach for it. For example:

```
LinkedList        time        space
append            O(1)        O(1)    keeps a tail reference
prepend           O(1)        O(1)
remove(value)     O(n)        O(1)    must walk to find it
get by position   O(n)        O(1)

When to use: cheap insert/remove at the front when you never need index access.
In Python, collections.deque usually covers this better.
```

If you're unsure of a cost, work it out from your own code, then check it against the Python Wiki's "Time Complexity" page.

### 3. 30 practice problems across 6+ patterns

Solve 30 problems from the NeetCode 150 (or Grind 75), covering at least six patterns: for example arrays and hashing, two pointers, sliding window, stack, binary search, linked list, trees, graphs, heaps.

For each problem, a short note in `problems/`:

- the problem in one sentence, and its link
- the pattern, and the clue in the statement that pointed to it
- your brute-force idea and its Big-O
- your final approach and its Big-O (time and space)
- your Python solution
- what tripped you up, if anything

Time-box each attempt (about 30–40 minutes). If you're stuck, read a hint or a solution, or ask an AI assistant to explain the idea, then close it and write the code yourself from scratch. A problem only counts once you've solved it without looking.

### 4. A benchmark script

`bench.py` measures, at three input sizes (for example 1,000, 10,000 and 100,000):

- `x in my_list` versus `x in my_set` for a value that isn't there (the worst case)
- your insertion sort versus `sorted()` on random data (insertion sort at 100,000 may take minutes, so use smaller sizes for it, and say so)

Use `time.perf_counter()` (or `timeit`), repeat each measurement a few times and keep the best. Write the results into `RESULTS.md` as a table, then two or three sentences on whether the numbers grew the way Big-O predicted. When the size goes up 10×, the O(n) times should go up about 10× and the O(n²) times about 100×.

### 5. A mistakes log

`MISTAKES.md` lists every problem you got wrong or needed help with: what went wrong (wrong pattern, off-by-one, missed edge case, too slow) and the date. A week later, re-solve each one from scratch and record whether you got it. This is the most valuable file in the repo: it's a list of exactly what to revise.

## Stretch goals

- Add a **min-heap** written by hand (`push`, `pop`, `peek`) and test it against `heapq`.
- Add **cycle detection** with three colours for a dependency graph, and use it to print a valid build order (a "topological sort").
- Add CI (GitHub Actions) that runs your tests on every push, with a badge in the README.

## How a reviewer will look at it

They'll pick three structures at random, read the code and the Big-O table, and ask you to explain one operation's cost out loud. They'll run the tests. Then they'll open three problem notes and the mistakes log to see how you think, not just whether you got the answer.
