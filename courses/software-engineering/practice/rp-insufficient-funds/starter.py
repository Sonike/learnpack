class InsufficientFunds(Exception):
    """Raised when a withdrawal is bigger than the balance."""

    def __init__(self, balance: float, amount: float):
        # TODO: store balance, amount and shortfall (amount - balance) on self
        # TODO: call super().__init__(message) with the message from the prompt
        super().__init__("not written yet")


def withdraw(balance: float, amount: float) -> float:
    """Return the new balance, or raise ValueError / InsufficientFunds."""
    # TODO: amount <= 0 -> ValueError("amount must be positive")
    # TODO: amount > balance -> InsufficientFunds(balance, amount)
    return balance


if __name__ == "__main__":
    print(withdraw(100.0, 30.0))
    try:
        withdraw(30.0, 50.0)
    except InsufficientFunds as e:
        print("Refused:", e)
