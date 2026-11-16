# Trees, graphs and heaps

## Why this matters

Lots of real data isn't a line of items: it's a hierarchy or a network. Folders inside folders, an org chart and a web page's HTML are **trees**. Roads between cities, friends of friends and packages that depend on other packages are **graphs**. "Find the shortest route", "are these connected?" and "can this be built, or is there a circular dependency?" are graph questions, and BFS and DFS answer them. **Heaps** round off the section: the right tool for "the top 10" or "whatever's most urgent next".

## 1. Binary trees

A **tree** is made of **nodes** connected by arrows from parent to child, with no loops. The top node is the **root**; nodes with no children are **leaves**. In a **binary tree**, each node has at most two children: `left` and `right`.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#        8
#       / \
#      3   10
#     / \    \
#    1   6    14
root = TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(6)), TreeNode(10, None, TreeNode(14)))
```

It's a linked list with two arrows per node instead of one. And notice that each child is the root of a smaller tree, a **subtree**. That's why recursion fits trees so well: solve it for the left subtree, solve it for the right, combine.

**Depth** (or height) is the number of nodes on the longest path from root to a leaf:

```python
def max_depth(node):
    if node is None:                     # empty tree: base case
        return 0
    return 1 + max(max_depth(node.left), max_depth(node.right))

print(max_depth(root))  # 3
```

Every node is visited once: O(n) time. The recursion goes as deep as the tree, so O(h) space for the call stack, where `h` is the height.

## 2. Traversals: visiting every node

There are four standard orders. The first three are recursive and differ only in *when* you handle the node itself:

```python
def preorder(node):    # node, then left, then right
    if node is None:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)

def inorder(node):     # left, then node, then right
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)

def postorder(node):   # left, then right, then node
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.val]

print(preorder(root))   # [8, 3, 1, 6, 10, 14]
print(inorder(root))    # [1, 3, 6, 8, 10, 14]
print(postorder(root))  # [1, 6, 3, 14, 10, 8]
```

- **Pre-order** handles a parent before its children: good for copying a tree or printing a folder listing.
- **Post-order** handles children first: good for "total size of this folder" (you need the subfolders' sizes first) or deleting a tree.
- **In-order** on the tree above came out sorted. That's no accident (next section).

The fourth is **level order**: row by row, top to bottom. It uses a queue, and it's breadth-first search on a tree:

```python
from collections import deque

def level_order(root):
    result = []
    queue = deque([root]) if root else deque()
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

print(level_order(root))  # [8, 3, 10, 1, 6, 14]
```

## 3. Binary search trees

A **binary search tree** (BST) is a binary tree with one rule, true at **every** node: everything in the left subtree is smaller, everything in the right subtree is bigger. The tree above follows it.

That rule makes searching like binary search: at each node, go left or right and ignore the other half.

```python
def contains(node, target):
    while node is not None:
        if target == node.val:
            return True
        node = node.left if target < node.val else node.right
    return False

print(contains(root, 6), contains(root, 7))  # True False
```

On a **balanced** tree (both sides roughly equal) that's O(log n). But insert 1, 2, 3, 4, 5 in order and every node goes right: the "tree" is a linked list and search is O(n). Real systems use self-balancing trees (database indexes use a close cousin called a B-tree), but juniors only need to know the problem exists.

Because smaller values are always left and bigger ones right, an in-order traversal of a BST visits values in sorted order. Checking whether a tree really is a BST is a common interview question; you'll do it in the "Binary tree basics" exercise. The trap is checking only each node against its direct children: a value deep on the left can still be bigger than an ancestor higher up.

## 4. Graphs

A **graph** is a set of **nodes** (also called vertices) joined by **edges**. Unlike a tree, there's no root, and edges can form loops. Edges can be **directed** (one-way: "A depends on B") or **undirected** (two-way: "A is friends with B").

The usual way to store one in Python is an **adjacency list**: a dict mapping each node to a list of its neighbours.

```python
#   A --- B
#   |     |
#   C --- D --- E
friends = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E"],
    "E": ["D"],
}
```

When we talk about graph algorithms, **V** is the number of vertices (nodes) and **E** the number of edges.

A **grid** is a graph in disguise: each cell is a node, and its neighbours are the cells up, down, left and right. Many interview questions ("shortest path through a maze", "count the islands") are graph problems on a grid.

## 5. Breadth-first search (BFS)

**BFS** explores in rings: first the start, then everything 1 step away, then everything 2 steps away, and so on. A **queue** gives exactly that order, because nodes found earlier are handled earlier. A **visited** set stops you processing a node twice (and going round loops forever).

```python
from collections import deque

def bfs_distances(graph, start):
    distance = {start: 0}           # also serves as the visited set
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph[node]:
            if neighbour not in distance:
                distance[neighbour] = distance[node] + 1
                queue.append(neighbour)
    return distance

print(bfs_distances(friends, "A"))
# {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 3}
```

Because BFS reaches nodes in order of distance, **the first time it reaches a node is by a shortest path**, counting edges. That's why BFS is the answer to "fewest steps" or "shortest path" whenever every step costs the same (an **unweighted** graph): mazes, degrees of separation, fewest moves in a puzzle.

**Cost:** each node is added to the queue once (O(V)), and each node's neighbour list is read once, which touches every edge once or twice (O(E)). So BFS is **O(V + E)** time and O(V) space. On a grid with `R × C` cells, that's O(R × C).

## 6. Depth-first search (DFS)

**DFS** goes as deep as it can down one path before backing up and trying the next, like exploring a maze by keeping one hand on the wall. Use a **stack**, or recursion (which uses the call stack for you).

```python
def dfs_reachable(graph, start):
    visited = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(neighbour)
    return visited

print(sorted(dfs_reachable(friends, "A")))  # ['A', 'B', 'C', 'D', 'E']
```

The code is BFS with the deque swapped for a list and `popleft` for `pop`. It's also O(V + E). DFS does **not** find shortest paths, but it's simpler for questions about **reachability and structure**:

- **Connected components:** "how many separate groups are there?" Loop over every node; each time you find one not yet visited, that's a new group, so DFS from it to mark the whole group. Counting islands on a grid works exactly this way.
- **Cycle detection:** "is there a circular dependency?"

**Cycle detection in a directed graph.** A build tool, package manager or spreadsheet must refuse `a needs b, b needs c, c needs a`. DFS with three **colours** finds it:

- **white:** not visited yet
- **grey:** on the path we're currently exploring
- **black:** finished: everything reachable from it is known to be cycle-free

If DFS steps onto a **grey** node, it has walked back onto its own path: a cycle.

```python
WHITE, GREY, BLACK = 0, 1, 2

def has_cycle(graph):
    colour = {}

    def visit(node):
        colour[node] = GREY
        for dep in graph.get(node, []):
            if colour.get(dep, WHITE) == GREY:
                return True
            if colour.get(dep, WHITE) == WHITE and visit(dep):
                return True
        colour[node] = BLACK
        return False

    return any(colour.get(n, WHITE) == WHITE and visit(n) for n in graph)

print(has_cycle({"app": ["db", "auth"], "auth": ["db"], "db": []}))  # False
print(has_cycle({"a": ["b"], "b": ["c"], "c": ["a"]}))               # True
```

Why not just "visited or not"? In the first graph, `db` is reached twice (from `app` and from `auth`), but that's a shared dependency, not a loop. The colours tell the two apart: the second time we reach `db`, it's black (finished), not grey.

**BFS or DFS?**

```
Question                                         Use
fewest steps / shortest path, all steps equal    BFS
"nearest" anything                                BFS
is B reachable from A at all?                    either (DFS is simpler)
count groups / islands / components               DFS (or BFS)
circular dependency? (cycle in a directed graph) DFS with colours
explore every possible path / arrangement        DFS (backtracking)
```

## 7. Heaps

Sometimes you don't need everything sorted, just quick access to the **smallest** (or most urgent) item, over and over, while items keep arriving. A **heap** does that.

A **min-heap** is a binary tree where every parent is smaller than or equal to its children, so the smallest item is always at the root. It's stored compactly in a plain list. Python's `heapq` module works on an ordinary list:

```python
import heapq

tasks = []
heapq.heappush(tasks, (2, "write tests"))     # (priority, task)
heapq.heappush(tasks, (1, "fix prod bug"))
heapq.heappush(tasks, (3, "update docs"))
print(tasks[0])                  # (1, 'fix prod bug')   peek: O(1)
print(heapq.heappop(tasks))      # (1, 'fix prod bug')   O(log n)
print(heapq.heappop(tasks))      # (2, 'write tests')
```

```
Operation                   Cost
peek at the smallest        O(1)
push / pop                  O(log n)
heapify a whole list        O(n)
```

`heapq` is a **min**-heap only. For "biggest first", push negated numbers, as in `(-score, name)`.

**Top k.** "The 3 most common words" doesn't need a full sort. `heapq.nsmallest(k, items, key=...)` and `heapq.nlargest` keep a heap of size `k`: O(n log k), which beats O(n log n) when `k` is small.

```python
import heapq
from collections import Counter

words = "the cat and the dog and the bird".split()
counts = Counter(words)
top = heapq.nsmallest(2, counts.items(), key=lambda item: (-item[1], item[0]))
print(top)  # [('the', 3), ('and', 2)]
```

The key `(-count, word)` means "highest count first, then alphabetical": the same trick you used with `sorted` in the lesson "Sorting". Heaps also power schedulers, merging many sorted lists and Dijkstra's shortest-path algorithm for weighted graphs (beyond this course).

## 8. What's next

That's the core interview toolkit: arrays, hash maps, two pointers, sliding windows, binary search, sorting, stacks, queues, linked lists, trees, BFS, DFS and heaps. The next topic most people meet is **dynamic programming**: recursion that remembers answers to sub-problems it has already solved (you saw the need for it with `count_paths` in the lesson "Recursion and binary search"). It's less common in junior interviews, so it isn't covered here; the freeCodeCamp dynamic programming course in this lesson's videos is a good place to start once you're comfortable with everything above.

After this section, practise with one problem list, such as the NeetCode 150 (linked in resources), grouped by pattern. Patterns beat volume: solve a few problems per pattern properly, then revisit the ones you got wrong a week later. Use an AI assistant to explain a solution you're stuck on, then close it and write the code yourself from memory.

## Common mistakes

**`AttributeError: 'NoneType' object has no attribute 'left'`.** You recursed into a missing child. Handle `None` as the base case at the top of the function.

**Forgetting the visited set.** BFS or DFS on a graph with a loop then runs forever (or until memory runs out). Mark a node visited **when you add it** to the queue or stack, not when you take it off, or the same node gets queued many times.

**Using DFS for shortest paths.** DFS finds *a* path, not the shortest. For fewest steps, use BFS.

**Using a list as the BFS queue.** `queue.pop(0)` makes BFS O(V²). Use `deque.popleft()`.

**Recursion depth on big inputs.** A recursive DFS over a 200 × 200 grid can need 40,000 frames and hit `RecursionError`. Use an explicit stack for grids and large graphs.

**Grid bounds.** `IndexError` or wrong answers from neighbours off the edge. Check `0 <= r < rows and 0 <= c < cols` before reading `grid[r][c]`. And remember negative indexes don't fail in Python: `grid[-1]` silently reads the last row.

**Treating `heapq` as a max-heap.** It always pops the smallest. Negate to get the largest.

## Recap

- A **binary tree** is nodes with `left`/`right` children; recursion on subtrees solves most tree problems. Pre-, in-, post- and level-order are the four traversals.
- A **BST** keeps smaller values left and bigger right at every node: O(log n) search when balanced, and in-order gives sorted output.
- **Graphs** are nodes and edges, stored as an adjacency list; grids are graphs.
- **BFS** (queue) explores in rings and finds shortest paths in unweighted graphs. **DFS** (stack or recursion) handles reachability, components and cycle detection. Both are O(V + E).
- A **heap** gives the smallest item in O(1) and push/pop in O(log n); `heapq.nsmallest`/`nlargest` solve top-k in O(n log k).
