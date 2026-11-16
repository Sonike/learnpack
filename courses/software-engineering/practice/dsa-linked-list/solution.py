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
        node = Node(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def prepend(self, value) -> None:
        self.head = Node(value, self.head)
        if self.tail is None:
            self.tail = self.head
        self.size += 1

    def remove(self, value) -> bool:
        prev, current = None, self.head
        while current is not None:
            if current.value == value:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                if current is self.tail:
                    self.tail = prev
                self.size -= 1
                return True
            prev, current = current, current.next
        return False

    def reverse(self) -> None:
        prev, current = None, self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev, current = current, next_node
        self.head, self.tail = self.tail, self.head

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self) -> int:
        return self.size
