PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(text: str) -> bool:
    """True if every bracket is closed by its partner in the right order."""
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in PAIRS:
            if not stack or stack[-1] != PAIRS[ch]:
                return False
            stack.pop()
    return not stack


def eval_rpn(tokens: list[str]) -> int:
    """Evaluate a reverse Polish notation expression."""
    stack = []
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(int(left / right))
        else:
            stack.append(int(token))
    return stack.pop()
