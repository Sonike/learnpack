class BankAccount:
    def __init__(self, owner: str):
        self.owner = owner
        # TODO: store the balance and history in "private" attributes (leading underscore)

    def deposit(self, amount: int) -> None:
        """Add amount cents. Raise ValueError if amount <= 0."""
        # TODO
        pass

    def withdraw(self, amount: int) -> None:
        """Take out amount cents. Raise ValueError if amount <= 0 or more than the balance."""
        # TODO
        pass

    @property
    def balance(self) -> int:
        """The current balance in cents (read-only)."""
        # TODO
        return 0

    @property
    def history(self) -> list[tuple[str, int]]:
        """A copy of the list of ("deposit" | "withdraw", amount) tuples."""
        # TODO
        return []

    def __repr__(self) -> str:
        # TODO: BankAccount(owner='Ada', balance=1250)
        return "BankAccount(?)"


if __name__ == "__main__":
    account = BankAccount("Ada")
    account.deposit(2000)
    account.withdraw(750)
    print(account)          # BankAccount(owner='Ada', balance=1250)
    print(account.history)  # [('deposit', 2000), ('withdraw', 750)]
    try:
        account.withdraw(5000)
    except ValueError as e:
        print("Refused:", e)
