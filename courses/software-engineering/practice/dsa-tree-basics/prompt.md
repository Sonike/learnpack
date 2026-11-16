# Binary tree basics

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The `TreeNode` class is written for you. An empty tree is just `None`.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None): ...

def max_depth(root: TreeNode | None) -> int: ...
def inorder(root: TreeNode | None) -> list: ...
def is_valid_bst(root: TreeNode | None) -> bool: ...
```

- `max_depth(root)`: the number of nodes on the longest path from the root down to a leaf. An empty tree has depth 0, a single node depth 1.
- `inorder(root)`: the values in **in-order**: everything in the left subtree, then the node itself, then everything in the right subtree.
- `is_valid_bst(root)`: `True` if the tree is a **binary search tree**: for **every** node, all values in its left subtree are strictly smaller and all values in its right subtree are strictly bigger. (Equal values are not allowed.) An empty tree is valid.

All three are short recursive functions. For `is_valid_bst`, checking each node against only its direct children isn't enough (see the second example below). Pass down the allowed range instead: a helper `check(node, low, high)` where every value must satisfy `low < val < high`. Going left, the current value becomes the new `high`; going right, it becomes the new `low`. Start with `low = -math.inf` and `high = math.inf`.

## Example

```
      8                    8
     / \                  / \
    3   10               3   10
   / \    \             / \
  1   6    14          1   9     <- 9 is bigger than 8 but sits on 8's left
```

```python
max_depth(left_tree)       # 3
inorder(left_tree)         # [1, 3, 6, 8, 10, 14]   in-order of a BST is sorted
is_valid_bst(left_tree)    # True
is_valid_bst(right_tree)   # False
```
