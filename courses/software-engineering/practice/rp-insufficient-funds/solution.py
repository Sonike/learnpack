class InsufficientFunds(Exception):
    """Raised when a withdrawal is bigger than the balance."""

    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        self.shortfall = amount - balance
        super().__init__(
            f"cannot withdraw {amount:.2f}: balance is {balance:.2f}, short by {self.shortfall:.2f}"
        )


def withdraw(balance: float, amount: float) -> float:
    """Return the new balance, or raise ValueError / InsufficientFunds."""
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFunds(balance, amount)
    return balance - amount
