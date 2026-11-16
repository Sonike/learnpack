# Your own exception class

Built-in exceptions say *what kind* of thing went wrong. Your own exception classes can say what went wrong **in your domain**, so callers can catch exactly that case.

```python
class InsufficientFunds(Exception):
    def __init__(self, balance: float, amount: float): ...

def withdraw(balance: float, amount: float) -> float:
```

- `InsufficientFunds` is a subclass of `Exception`. Its `__init__` stores `balance`, `amount` and `shortfall` (`amount - balance`) as attributes, and passes a message to `super().__init__(...)` like `"cannot withdraw 50.00: balance is 30.00, short by 20.00"`. Format the numbers with two decimals (`f"{x:.2f}"`).
- `withdraw` returns the new balance (`balance - amount`).
  - If `amount` is zero or negative, raise `ValueError("amount must be positive")`.
  - If `amount` is more than `balance`, raise `InsufficientFunds(balance, amount)`.
  - Withdrawing exactly the whole balance is allowed.

## Example

```python
withdraw(100.0, 30.0)   # 70.0
withdraw(30.0, 50.0)    # InsufficientFunds: cannot withdraw 50.00: balance is 30.00, short by 20.00
```

```python
try:
    withdraw(30.0, 50.0)
except InsufficientFunds as e:
    print(e.shortfall)   # 20.0
```
