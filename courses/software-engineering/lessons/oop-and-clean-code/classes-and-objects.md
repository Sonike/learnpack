# Classes and objects

## Why this matters

So far you've kept data in dicts and lists and written functions that work on them. That works until the data has rules. A bank balance must never go below zero, a fraction must never have a zero denominator, and nothing stops some far-off line of code from writing `account["balance"] = -500`. A **class** lets you bundle data together with the only functions allowed to change it, so the rules live in one place. Every Python library you'll use at work is built from classes, so reading and writing them is a daily skill.

## From a dict to a class

Here's an account as a dict, plus a function that changes it:

```python
account = {"owner": "Ada", "balance": 0}

def deposit(account, amount):
    account["balance"] += amount

deposit(account, 50)
print(account)   # {'owner': 'Ada', 'balance': 50}
```

The data and the function that changes it are separate. Nothing ties `deposit` to accounts, and anyone can skip it and edit `account["balance"]` directly.

Now the same thing as a class:

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount


account = BankAccount("Ada")
account.deposit(50)
print(account.owner, account.balance)   # Ada 50
```

Some words you'll need:

- A **class** is a blueprint: `BankAccount` describes what every account has and can do.
- An **object** (or **instance**) is one thing built from the blueprint. `BankAccount("Ada")` creates one. You can create as many as you like, and each has its own data.
- An **attribute** is a variable that belongs to an object: `account.owner`, `account.balance`.
- A **method** is a function defined inside a class: `deposit`. You call it with a dot: `account.deposit(50)`.

Class names use `CapitalisedWords` (called PascalCase); functions and attributes use `snake_case`. That's a convention from PEP 8, Python's style guide, and every Python developer follows it.

## `__init__` and `self`

`__init__` (say "dunder init", for the **d**ouble **under**scores) is the method Python runs automatically when you create an object. Its job is to set up the starting attributes.

`self` is the object the method is working on. When you write `account.deposit(50)`, Python turns it into `BankAccount.deposit(account, 50)`. The object before the dot becomes the first argument:

```python
a = BankAccount("Ada")
b = BankAccount("Grace")
a.deposit(50)                     # inside deposit, self is a
BankAccount.deposit(b, 20)        # exactly the same as b.deposit(20)
print(a.balance, b.balance)       # 50 20
```

That's all `self` is. It isn't a keyword; it's just the name everyone uses for the first parameter. Forget it in a method definition and you'll see this error:

```python
class Broken:
    def hello():          # no self
        return "hi"

Broken().hello()
# TypeError: Broken.hello() takes 0 positional arguments but 1 was given
```

Read it literally: you passed zero arguments, but Python passed one (the object). The fix is `def hello(self):`.

> **Try it:** create two accounts, deposit into one, and print both balances. Each object keeps its own attributes.

## Making objects print nicely: `__repr__` and `__str__`

Print an object with no extra work and you get something unhelpful:

```python
print(BankAccount("Ada"))   # <__main__.BankAccount object at 0x10a3c2d50>
```

Python lets you customise this with **special methods**, the ones named with double underscores. Python calls them for you at the right moment.

- `__repr__` returns a string for developers: what you see in the REPL, in lists and in error messages. A good `repr` looks like the code that would build the object.
- `__str__` returns a string for users, used by `print()` and `str()`. If you don't define it, Python uses `__repr__`.

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"


print(BankAccount("Ada"))        # BankAccount(owner='Ada', balance=0)
print([BankAccount("Grace")])    # [BankAccount(owner='Grace', balance=0)]
```

`{self.owner!r}` puts the `repr` of the owner in the string, which adds the quotes around `'Ada'`. Define `__repr__` on every class you write; it pays for itself the first time you debug.

## Comparing objects: `__eq__`

By default `==` on two objects asks "are these the very same object?", not "do they hold the same values?":

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

print(Point(1, 2) == Point(1, 2))   # False
```

Define `__eq__` to say what "equal" means for your class:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


print(Point(1, 2) == Point(1, 2))   # True
print(Point(1, 2) == "a string")    # False
```

Returning `NotImplemented` (a special built-in value, not an error) tells Python "I don't know how to compare with that", and Python then falls back to `False`. Other special methods work the same way: `__add__` powers `+`, `__lt__` powers `<`, `__len__` powers `len()`. You'll write `__add__` in the Fraction exercise.

## Class attributes vs instance attributes

An attribute set on `self` inside a method belongs to one object. An attribute written directly in the class body belongs to the class and is **shared by every object**:

```python
class Account:
    interest_rate = 0.02          # class attribute: one value for all accounts

    def __init__(self, owner):
        self.owner = owner        # instance attribute: one per object

a = Account("Ada")
b = Account("Grace")
print(a.interest_rate, b.interest_rate)   # 0.02 0.02
Account.interest_rate = 0.03
print(a.interest_rate)                     # 0.03
```

Class attributes are good for constants shared by every instance. They're a trap for anything mutable, like a list:

```python
class Account:
    history = []                  # shared by EVERY account

    def __init__(self, owner):
        self.owner = owner

    def deposit(self, amount):
        self.history.append(amount)

a = Account("Ada")
b = Account("Grace")
a.deposit(50)
print(b.history)   # [50]   Grace sees Ada's deposit!
```

There's only one list, attached to the class, so every account appends to it. The fix: create mutable attributes inside `__init__`, so each object gets its own:

```python
    def __init__(self, owner):
        self.owner = owner
        self.history = []         # a new list for each account
```

## Encapsulation: protecting the data

**Encapsulation** means keeping an object's data behind its methods, so the object can enforce its own rules. Python doesn't have truly private attributes. Instead it has a convention: a name that starts with one underscore, like `_balance`, means "internal: don't touch this from outside the class". Nothing stops you, but every Python developer reads it as a warning sign.

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
```

Now all changes go through `deposit` and `withdraw`, which check the rules. But how does outside code *read* the balance without touching `_balance`?

## `@property`: attributes with rules

A **property** is a method that you read like an attribute. You make one with the `@property` **decorator** (a line starting with `@` that wraps the function below it):

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount


account = BankAccount("Ada")
account.deposit(50)
print(account.balance)      # 50   (no parentheses: it reads like an attribute)
account.balance = 1_000_000
# AttributeError: property 'balance' of 'BankAccount' object has no setter
```

Because there's no setter, `balance` is **read-only**. Outside code can look but not change. If you do want assignment with a check, add a setter:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age             # this goes through the setter below

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("age cannot be negative")
        self._age = value


p = Person("Ada", 36)
p.age = 37          # fine
p.age = -1          # ValueError: age cannot be negative
```

The nice part: code that used `p.age` before you added the property keeps working unchanged. You can start with a plain attribute and switch to a property later, when a rule appears.

> **Note:** a property that returns a list hands out the real list, and outside code can still `.append` to it. If that would break your rules, return a copy: `return list(self._history)`. You'll do this in the bank account exercise.

## Common mistakes

**Forgetting `self.` inside a method.**

```python
    def deposit(self, amount):
        balance += amount
# UnboundLocalError: cannot access local variable 'balance' where it is not associated with a value
```

Without `self.`, Python thinks `balance` is a new local variable. Attributes always need `self.` in front.

**Forgetting the parentheses when creating an object.** `account = BankAccount` (no parentheses) gives you the class itself, not an object. The next line, `account.deposit(50)`, then fails with `TypeError: BankAccount.deposit() missing 1 required positional argument: 'amount'`, because there was no object to fill `self`, so `50` went into `self` and `amount` was missing.

**Mutable class attributes**, as above. If two objects mysteriously share data, look for a list or dict in the class body.

**Calling a property with parentheses.** `account.balance()` fails with `TypeError: 'int' object is not callable`: `account.balance` already ran the method and gave you an `int`, and then you tried to call that `int`.

**Making everything a class.** If something has no data to protect and no state to remember, a plain function is simpler. Classes earn their place when data and rules belong together.

> **Note:** when you ask an AI assistant about classes, ask it to *explain* an error or a concept ("why does my list get shared between objects?"), then write the fix yourself. Typing the class out is how the shape of `__init__`, `self` and properties sticks.

## Recap

- A **class** bundles data (attributes) with the functions that act on it (methods). Each **object** made from it has its own attributes.
- `__init__` sets up a new object. `self` is the object before the dot.
- Special methods hook into Python: `__repr__` for debugging output, `__eq__` for `==`, `__add__` for `+`.
- Class-body attributes are shared by all objects; create lists and dicts in `__init__`.
- Use `_name` for internal data and `@property` to expose it read-only or with validation.
