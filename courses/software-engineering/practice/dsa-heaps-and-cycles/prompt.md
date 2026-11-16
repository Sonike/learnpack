# Top k with a heap, and cycles in a dependency graph

## 1. Top k frequent words

```python
def top_k_frequent(words: list[str], k: int) -> list[str]: ...
```

- Return the `k` most common words, most common first. Break ties **alphabetically** (`"apple"` before `"banana"`).
- If there are fewer than `k` different words, return all of them.
- Count with `collections.Counter`, then use `heapq.nsmallest(k, counts.items(), key=...)` with the key `(-count, word)`: the minus sign makes the biggest count the "smallest". That's O(n log k) instead of sorting everything.

```python
top_k_frequent(["a", "b", "a", "c", "b", "a"], 2)   # ["a", "b"]
top_k_frequent(["dog", "cat", "dog", "cat", "eel"], 2)  # ["cat", "dog"]   tie: alphabetical
```

## 2. Does this dependency graph have a cycle?

```python
def has_cycle(graph: dict[str, list[str]]) -> bool: ...
```

- `graph` maps each task to the tasks it depends on: `{"app": ["db", "auth"], "auth": ["db"], "db": []}`. This is a **directed graph** stored as an **adjacency list**.
- A name may appear only as a dependency and never as a key; treat it as having no dependencies (use `graph.get(name, [])`).
- Return `True` if following dependencies can lead back to where you started (`a → b → a`, or `a → a`). A build tool can't order tasks in a cycle.

Use DFS with three **colours**: `WHITE` = not visited yet, `GREY` = on the current path, `BLACK` = finished and known to be safe. Visiting a node: paint it grey, visit each dependency, then paint it black. If you ever step onto a **grey** node, you've walked in a circle.

```python
has_cycle({"app": ["db", "auth"], "auth": ["db"], "db": []})  # False
has_cycle({"a": ["b"], "b": ["c"], "c": ["a"]})               # True
```
