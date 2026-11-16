import math


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: TreeNode | None) -> int:
    """Number of nodes on the longest root-to-leaf path (0 for an empty tree)."""
    # TODO: None -> 0; otherwise 1 + the bigger of the two children's depths
    return 0


def inorder(root: TreeNode | None) -> list:
    """Values in left, node, right order."""
    # TODO: None -> []; otherwise inorder(left) + [root.val] + inorder(right)
    return []


def is_valid_bst(root: TreeNode | None) -> bool:
    """True if every node is strictly between everything on its left and its right."""

    def check(node, low, high):
        # TODO: None -> True
        # TODO: if not (low < node.val < high) -> False
        # TODO: check the left child with high=node.val and the right child with low=node.val
        return True

    return check(root, -math.inf, math.inf)


if __name__ == "__main__":
    tree = TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(6)), TreeNode(10, None, TreeNode(14)))
    print(max_depth(tree))     # want 3
    print(inorder(tree))       # want [1, 3, 6, 8, 10, 14]
    print(is_valid_bst(tree))  # want True
