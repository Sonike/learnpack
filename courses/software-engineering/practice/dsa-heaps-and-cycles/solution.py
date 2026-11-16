import heapq
from collections import Counter

WHITE, GREY, BLACK = 0, 1, 2


def top_k_frequent(words: list[str], k: int) -> list[str]:
    """The k most common words, most common first, ties alphabetical."""
    counts = Counter(words)
    best = heapq.nsmallest(k, counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in best]


def has_cycle(graph: dict[str, list[str]]) -> bool:
    """True if following dependencies can lead back to a task already on the path."""
    colour = {}  # name -> WHITE/GREY/BLACK; missing means WHITE

    def visit(node) -> bool:
        colour[node] = GREY
        for dep in graph.get(node, []):
            state = colour.get(dep, WHITE)
            if state == GREY:
                return True
            if state == WHITE and visit(dep):
                return True
        colour[node] = BLACK
        return False

    return any(colour.get(node, WHITE) == WHITE and visit(node) for node in graph)
