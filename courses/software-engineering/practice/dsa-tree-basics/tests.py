from solution import TreeNode, inorder, is_valid_bst, max_depth


def bst():
    return TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(6)), TreeNode(10, None, TreeNode(14)))


def test_max_depth():
    got = max_depth(bst())
    assert got == 3, f"expected 3, got {got!r}"
    chain = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
    got = max_depth(chain)
    assert got == 4, f"a chain of 4 nodes has depth 4, got {got!r}"


def test_inorder_of_a_bst_is_sorted():
    got = inorder(bst())
    assert got == [1, 3, 6, 8, 10, 14], f"expected [1, 3, 6, 8, 10, 14], got {got!r}"


def test_empty_tree():
    got = (max_depth(None), inorder(None), is_valid_bst(None))
    assert got == (0, [], True), f"expected (0, [], True), got {got!r}"


def test_valid_bst():
    got = is_valid_bst(bst())
    assert got is True, f"expected True, got {got!r}"


def test_rejects_a_value_on_the_wrong_side_of_an_ancestor():
    tree = TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(9)), TreeNode(10))
    got = is_valid_bst(tree)
    assert got is False, f"9 sits left of 8: expected False, got {got!r}"


def test_rejects_duplicates_and_wrong_children():
    for tree in [TreeNode(5, TreeNode(5)), TreeNode(5, None, TreeNode(2))]:
        got = is_valid_bst(tree)
        assert got is False, f"expected False, got {got!r}"
