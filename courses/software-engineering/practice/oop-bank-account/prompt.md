# A bank account that protects its balance

Write a class `BankAccount` that keeps its own balance safe. Code outside the class should only be able to change the balance through `deposit` and `withdraw`, and every change is recorded in a history.

```python
class BankAccount:
    def __init__(self, owner: str): ...
    def deposit(self, amount: int) -> None: ...
    def withdraw(self, amount: int) -> None: ...
    @property
    def balance(self) -> int: ...
    @property
    def history(self) -> list[tuple[str, int]]: ...
    def __repr__(self) -> str: ...
```

- `owner` is the account holder's name. A new account starts with a balance of `0`.
- Amounts are whole numbers of **cents** (so `1250` means 12.50). Using cents avoids rounding errors with floats.
- `deposit(amount)` adds money. If `amount` is zero or negative, raise `ValueError`.
- `withdraw(amount)` takes money out. If `amount` is zero or negative, raise `ValueError`. If it is more than the balance, raise `ValueError` and leave the balance unchanged (no overdrafts).
- `balance` is a **read-only property**: `account.balance` works, but `account.balance = 1_000_000` must fail with `AttributeError`. A property with no setter does that for you.
- `history` is a property that returns a list of `(kind, amount)` tuples in order, where `kind` is `"deposit"` or `"withdraw"`. Failed operations are not recorded. Return a **copy**, so code outside the class can't edit the real history.
- `repr(account)` returns `BankAccount(owner='Ada', balance=1250)`.

## Example

```python
account = BankAccount("Ada")
account.deposit(2000)
account.withdraw(750)
account.balance      # 1250
account.history      # [("deposit", 2000), ("withdraw", 750)]
account.withdraw(5000)  # ValueError: insufficient funds
account                 # BankAccount(owner='Ada', balance=1250)
```
