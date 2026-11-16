class BankAccount:
    def __init__(self, owner: str):
        self.owner = owner
        self._balance = 0
        self._history: list[tuple[str, int]] = []

    def deposit(self, amount: int) -> None:
        """Add amount cents. Raise ValueError if amount <= 0."""
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount
        self._history.append(("deposit", amount))

    def withdraw(self, amount: int) -> None:
        """Take out amount cents. Raise ValueError if amount <= 0 or more than the balance."""
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        self._history.append(("withdraw", amount))

    @property
    def balance(self) -> int:
        """The current balance in cents (read-only)."""
        return self._balance

    @property
    def history(self) -> list[tuple[str, int]]:
        """A copy of the list of ("deposit" | "withdraw", amount) tuples."""
        return list(self._history)

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"


if __name__ == "__main__":
    account = BankAccount("Ada")
    account.deposit(2000)
    account.withdraw(750)
    print(account)
    print(account.history)
