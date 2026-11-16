def add(numbers: str) -> int:
    """Sum the numbers in a string. See the prompt for the five stages."""
    # TODO: stage 1 first. Write its checks below, watch them fail, then make them pass.
    return 0


def check(text: str, want: int) -> None:
    """Print PASS or FAIL for one example, so one red check doesn't stop the rest."""
    got = add(text)
    print("PASS" if got == want else "FAIL", f"add({text!r}) == {want}", "" if got == want else f"(got {got!r})")


if __name__ == "__main__":
    # Stage 1
    check("", 0)
    check("4", 4)
    check("1,2", 3)
    # TODO: add checks for stages 2-5 one at a time, red -> green -> refactor.
    # For stage 5, call add inside try/except ValueError and print the message.
