import math


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: TreeNode | None) -> int:
    """Number of nodes on the longest root-to-leaf path (0 for an empty tree)."""
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def inorder(root: TreeNode | None) -> list:
    """Values in left, node, right order."""
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def is_valid_bst(root: TreeNode | None) -> bool:
    """True if every node is strictly between everything on its left and its right."""

    def check(node, low, high):
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    return check(root, -math.inf, math.inf)
