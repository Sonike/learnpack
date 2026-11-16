PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(text: str) -> bool:
    """True if every bracket is closed by its partner in the right order."""
    stack = []
    # TODO: for ch in text:
    #         opening bracket -> push it
    #         closing bracket -> if the stack is empty or the top isn't PAIRS[ch], return False; else pop
    # TODO: balanced only if the stack ends up empty
    return False


def eval_rpn(tokens: list[str]) -> int:
    """Evaluate a reverse Polish notation expression."""
    stack = []
    # TODO: for token in tokens:
    #         operator -> right = stack.pop(); left = stack.pop(); push the result
    #         number -> push int(token)
    return 0


if __name__ == "__main__":
    print(is_balanced("print(items[0])"))       # want True
    print(is_balanced("([)]"))                  # want False
    print(eval_rpn(["2", "3", "+", "4", "*"]))  # want 20
