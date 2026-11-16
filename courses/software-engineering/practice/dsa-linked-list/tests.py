from solution import LinkedList


def test_append_and_prepend():
    ll = LinkedList([1, 2, 3])
    ll.prepend(0)
    ll.append(4)
    got = (list(ll), len(ll))
    assert got == ([0, 1, 2, 3, 4], 5), f"expected ([0, 1, 2, 3, 4], 5), got {got!r}"


def test_remove_first_middle_and_last():
    ll = LinkedList(["a", "b", "c", "d"])
    results = [ll.remove("a"), ll.remove("c"), ll.remove("d")]
    assert results == [True, True, True], f"expected all True, got {results!r}"
    assert list(ll) == ["b"], f"expected ['b'], got {list(ll)!r}"
    ll.append("e")  # the tail must have been fixed when "d" went
    assert list(ll) == ["b", "e"], f"append after removing the tail gave {list(ll)!r}"


def test_remove_missing_value_returns_false():
    ll = LinkedList([1, 2])
    got = (ll.remove(9), list(ll), len(ll))
    assert got == (False, [1, 2], 2), f"expected (False, [1, 2], 2), got {got!r}"


def test_remove_only_removes_the_first_match():
    ll = LinkedList([7, 1, 7])
    ll.remove(7)
    assert list(ll) == [1, 7], f"expected [1, 7], got {list(ll)!r}"


def test_reverse_in_place():
    ll = LinkedList([1, 2, 3, 4])
    head = ll.head
    ll.reverse()
    assert list(ll) == [4, 3, 2, 1], f"expected [4, 3, 2, 1], got {list(ll)!r}"
    assert ll.tail is head, "reverse should reuse the same nodes, so the old head becomes the tail"
    ll.append(0)
    assert list(ll) == [4, 3, 2, 1, 0], f"append after reverse gave {list(ll)!r}"


def test_empty_list_edge_cases():
    ll = LinkedList()
    ll.reverse()
    got = (list(ll), len(ll), ll.remove(1))
    assert got == ([], 0, False), f"expected ([], 0, False), got {got!r}"
    ll.prepend("x")
    ll.append("y")
    assert list(ll) == ["x", "y"], f"expected ['x', 'y'], got {list(ll)!r}"
