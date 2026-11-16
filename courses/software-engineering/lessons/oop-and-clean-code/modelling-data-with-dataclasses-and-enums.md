# Modelling data with dataclasses and enums

## Why this matters

Most of the classes you'll write at work mainly hold data: a user, an order, a task, a reading from a sensor. Writing `__init__`, `__repr__` and `__eq__` by hand for each one is repetitive and easy to get subtly wrong. Python's `dataclasses` module writes them for you, and `enum` gives you a safe way to say "this field can only be one of these values". Together they let you design data so that **invalid states are hard to even write down**, which removes whole families of bugs before you've written a single test.

## The boilerplate problem

Here's a plain class for a task:

```python
class Task:
    def __init__(self, id, title, done=False):
        self.id = id
        self.title = title
        self.done = done

    def __repr__(self):
        return f"Task(id={self.id!r}, title={self.title!r}, done={self.done!r})"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return (self.id, self.title, self.done) == (other.id, other.title, other.done)
```

Fifteen lines, and every field name is written four times. Add a field and you must remember to update all four places.

## `@dataclass`

The same class as a **dataclass**:

```python
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


t = Task(1, "Buy milk")
print(t)                              # Task(id=1, title='Buy milk', done=False)
print(t == Task(1, "Buy milk"))       # True
t.done = True
print(t)                              # Task(id=1, title='Buy milk', done=True)
```

The `@dataclass` decorator reads the **fields** you list in the class body (each one is `name: type`) and generates `__init__`, `__repr__` and `__eq__` for you. The type after the colon is a **type hint**: it documents what each field holds. Python doesn't check it when the program runs (the lesson "Type hints" covers how tools do), but the dataclass needs it to know what the fields are.

Fields with defaults (`done: bool = False`) must come after fields without them, for the same reason as function parameters: `Task(1, "Buy milk")` has to know which value goes where.

A dataclass is still a normal class. You can add methods:

```python
@dataclass
class Task:
    id: int
    title: str
    done: bool = False

    def complete(self):
        self.done = True
```

## Defaults that are lists: `field(default_factory=...)`

Suppose each task can have tags. The obvious version fails as soon as Python reads the class:

```python
@dataclass
class Task:
    title: str
    tags: list[str] = []
# ValueError: mutable default <class 'list'> for field tags is not allowed: use default_factory
```

That's the dataclass protecting you from the shared-list bug from the lesson "Classes and objects": a default of `[]` would be one list shared by every task. The error message even tells you the fix. `field(default_factory=list)` means "call `list()` to make a **fresh** empty list for each new object":

```python
from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    tags: list[str] = field(default_factory=list)


a = Task("Buy milk")
b = Task("Write tests")
a.tags.append("shopping")
print(a.tags, b.tags)   # ['shopping'] []
```

## Frozen dataclasses: values that never change

Some data should never change once created. A sum of money, a date, a coordinate: you don't edit `5 EUR` into `7 EUR`, you make a new value. `frozen=True` enforces that:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str


price = Money(1250, "EUR")
price.amount_cents = 0
# dataclasses.FrozenInstanceError: cannot assign to field 'amount_cents'
```

An object that can't change is called **immutable**. Immutable objects are easier to reason about: if you pass `price` to a function, you know for sure it comes back unchanged. They're also **hashable**, which means they can go in a `set` or be used as dict keys:

```python
prices = {Money(100, "EUR"), Money(100, "EUR"), Money(100, "USD")}
print(len(prices))   # 2
```

To "change" a frozen value, build a new one. Methods on a frozen class return new objects:

```python
@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"cannot add {self.currency} and {other.currency}")
        return Money(self.amount_cents + other.amount_cents, self.currency)


print(Money(1250, "EUR") + Money(100, "EUR"))   # Money(amount_cents=1350, currency='EUR')
```

That `ValueError` is the point. Plain numbers would let you add euros to dollars without a word of complaint. `Money` makes the mistake impossible to miss.

> **Note:** money is stored as whole **cents** in an `int`, never as a float like `12.5`. Floats can't represent most decimal fractions exactly: `0.1 + 0.2` is `0.30000000000000004`. For money, that's a real bug.

## Ordering: `order=True`

Want to sort dataclass objects? `order=True` generates `<`, `>`, `<=` and `>=`, comparing fields in the order you declared them:

```python
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int


versions = [Version(1, 10, 0), Version(1, 2, 3), Version(0, 9, 9)]
print(max(versions))   # Version(major=1, minor=10, patch=0)
```

Compare that with sorting version strings, where `"1.10.0" < "1.2.3"` is `True`, because strings compare character by character.

## Enums: a fixed set of choices

A task's status might be "todo", "doing" or "done". Store it as a string and nothing stops a typo:

```python
task_status = "Done"      # capital D
if task_status == "done":
    print("finished")     # never prints, and no error tells you why
```

An **enum** (short for enumeration) defines a fixed set of named values:

```python
from enum import Enum


class Status(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


s = Status.DONE
print(s)                   # Status.DONE
print(s.value)             # done
print(s == Status.DONE)    # True
print(Status("todo"))      # Status.TODO   (look a value up, e.g. from a database)
print(list(Status))        # [<Status.TODO: 'todo'>, <Status.DOING: 'doing'>, <Status.DONE: 'done'>]
```

Now a typo is loud:

```python
Status.DNOE
# AttributeError: type object 'Status' has no attribute 'DNOE'
Status("finished")
# ValueError: 'finished' is not a valid Status
```

Your editor also autocompletes `Status.` and shows you every valid choice. Enum members are written in `UPPER_CASE` because they're constants.

Combine them:

```python
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    TODO = "todo"
    DONE = "done"


@dataclass
class Task:
    id: int
    title: str
    status: Status = Status.TODO


tasks = [Task(1, "Buy milk"), Task(2, "Write tests", Status.DONE)]
done = [t.title for t in tasks if t.status is Status.DONE]
print(done)   # ['Write tests']
```

## Choosing the right container

| Use | When | Example |
|---|---|---|
| `tuple` | a small, fixed group where position is obvious | `(x, y)` coordinates |
| `dict` | data whose keys you don't know in advance, or raw JSON you've just loaded | word counts, a parsed API response |
| `@dataclass` | a record with known, named fields | `Task`, `User`, `Order` |
| `@dataclass(frozen=True)` | a value that shouldn't change | `Money`, `DateRange` |
| a normal class | an object with rules and hidden state | `BankAccount` with a protected balance |
| `Enum` | one choice from a fixed list | `Status`, `Role`, `Priority` |

A common, healthy pattern: load JSON into dicts at the edge of your program, convert them to dataclasses straight away, and let the rest of your code work with the typed objects.

## Making invalid states hard to represent

This is the design idea behind everything above. Look at this model:

```python
@dataclass
class Order:
    paid: bool
    shipped: bool
    refunded: bool
```

Three booleans allow eight combinations. Can an order be shipped but not paid? Refunded but never paid? The data allows it, so some day a bug will produce it, and every function will need checks for nonsense combinations. Compare:

```python
class OrderState(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    REFUNDED = "refunded"


@dataclass
class Order:
    state: OrderState = OrderState.PENDING
```

Exactly four states, all of them meaningful. The nonsense combinations can't be written down at all. When you design data, ask "which combinations of these fields are impossible in real life?" and try to make them impossible in code too. The same thinking leads to `Money` instead of a bare `int`, and to validating in `__post_init__`:

```python
@dataclass(frozen=True)
class DateRange:
    start: int
    end: int

    def __post_init__(self):
        if self.end < self.start:
            raise ValueError("end must not be before start")


DateRange(5, 3)   # ValueError: end must not be before start
```

`__post_init__` is a method the generated `__init__` calls right after filling in the fields, the natural place for checks.

> **Try it:** build an `Order` with three booleans and write down every combination that makes no sense. Then rewrite it with an enum and count how many are left.

## Common mistakes

**A mutable default.** `tags: list[str] = []` raises `ValueError: mutable default ... use default_factory`. Use `field(default_factory=list)`.

**A field without a default after one with a default.** `TypeError: non-default argument 'title' follows default argument`. Move fields with defaults to the end.

**Comparing an enum to its value.** `Status.DONE == "done"` is `False`: an enum member isn't equal to its raw value. Compare members to members (`status is Status.DONE`), or convert with `Status("done")` when reading from outside.

**Forgetting the type hint.** In a dataclass, `title = "untitled"` without `: str` isn't a field; it's an ordinary class attribute, and it won't appear in `__init__`. Every field needs a hint.

**Changing a frozen object.** `FrozenInstanceError` means the design is working. Build a new object with the new values instead, or use `dataclasses.replace(obj, field=new_value)`, which copies the object with one field changed.

## Recap

- `@dataclass` writes `__init__`, `__repr__` and `__eq__` from the fields you declare.
- Mutable defaults need `field(default_factory=list)`.
- `frozen=True` makes objects immutable and hashable, ideal for values like money. `order=True` makes them sortable.
- `Enum` turns a fixed set of choices into named constants, so typos fail loudly.
- Choose dict, tuple, dataclass or class on purpose, and design your data so impossible states can't be written down.
