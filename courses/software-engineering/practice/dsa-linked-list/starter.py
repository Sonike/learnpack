class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next  # the next Node, or None at the end


class LinkedList:
    def __init__(self, values=()):
        self.head = None
        self.tail = None
        self.size = 0
        for value in values:
            self.append(value)

    def append(self, value) -> None:
        # TODO: make a Node; if the list is empty it's both head and tail,
        #       otherwise link it after self.tail and move tail. Add 1 to size.
        pass

    def prepend(self, value) -> None:
        # TODO: make a Node whose next is the old head; it becomes the head (and tail if empty)
        pass

    def remove(self, value) -> bool:
        # TODO: walk with prev and current; when current.value == value, unlink it
        #       (fix self.head if prev is None, fix self.tail if current was the tail)
        return False

    def reverse(self) -> None:
        # TODO: prev = None; current = self.head
        #       while current: save next, point current.next at prev, step forward
        #       finally swap head and tail
        pass

    def __iter__(self):
        current = self.head
        # TODO: while current: yield current.value; move to current.next
        return iter([])

    def __len__(self) -> int:
        return self.size


if __name__ == "__main__":
    ll = LinkedList([1, 2, 3])
    ll.prepend(0)
    ll.append(4)
    print(list(ll))       # want [0, 1, 2, 3, 4]
    print(ll.remove(2))   # want True
    ll.reverse()
    print(list(ll), len(ll))  # want [4, 3, 1, 0] 4
