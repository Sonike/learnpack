# Two stack problems

A **stack** is last-in, first-out: you only touch the top. In Python, a list is a perfect stack: `append` pushes onto the top and `pop()` takes the top off, both O(1).

## 1. Balanced brackets

```python
def is_balanced(text: str) -> bool: ...
```

Return `True` if every `(`, `[` and `{` in `text` is closed by the matching `)`, `]` or `}` in the right order. Ignore every other character.

```python
is_balanced("print(items[0])")   # True
is_balanced("{[()]}")            # True
is_balanced("([)]")              # False   closed in the wrong order
is_balanced("((")                # False   never closed
is_balanced(")")                 # False   closed before opened
```

Push each opening bracket. On a closing bracket, the top of the stack must be its partner: pop it. At the end the stack must be empty.

## 2. Reverse Polish notation calculator

```python
def eval_rpn(tokens: list[str]) -> int: ...
```

In **reverse Polish notation** the operator comes after its two numbers: `3 4 +` means `3 + 4`, and `2 3 + 4 *` means `(2 + 3) * 4`. No brackets are ever needed.

- `tokens`: a valid expression, split into strings: integers (possibly negative, like `"-3"`) and the operators `"+"`, `"-"`, `"*"`, `"/"`.
- Push numbers. On an operator, pop the **right** number first, then the **left** one, compute `left op right`, and push the result. At the end, the answer is the one number left.
- Division truncates toward zero: use `int(left / right)` (so `-7 / 2` is `-3`, not `-4`).

```python
eval_rpn(["2", "3", "+", "4", "*"])  # 20
eval_rpn(["10", "3", "-"])           # 7
eval_rpn(["-7", "2", "/"])           # -3
```
