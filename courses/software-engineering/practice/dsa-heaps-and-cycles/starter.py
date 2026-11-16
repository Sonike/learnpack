import heapq
from collections import Counter

WHITE, GREY, BLACK = 0, 1, 2


def top_k_frequent(words: list[str], k: int) -> list[str]:
    """The k most common words, most common first, ties alphabetical."""
    counts = Counter(words)
    # TODO: best = heapq.nsmallest(k, counts.items(), key=lambda item: (-item[1], item[0]))
    # TODO: return just the words
    return []


def has_cycle(graph: dict[str, list[str]]) -> bool:
    """True if following dependencies can lead back to a task already on the path."""
    colour = {}  # name -> WHITE/GREY/BLACK; missing means WHITE

    def visit(node) -> bool:
        # TODO: paint node GREY
        # TODO: for dep in graph.get(node, []):
        #         GREY dep -> return True (cycle); WHITE dep -> if visit(dep): return True
        # TODO: paint node BLACK, return False
        return False

    # TODO: call visit on every WHITE node in graph; return True if any finds a cycle
    return False


if __name__ == "__main__":
    print(top_k_frequent(["a", "b", "a", "c", "b", "a"], 2))  # want ['a', 'b']
    print(has_cycle({"app": ["db", "auth"], "auth": ["db"], "db": []}))  # want False
    print(has_cycle({"a": ["b"], "b": ["c"], "c": ["a"]}))  # want True
