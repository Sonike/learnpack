# Inheritance, composition and interfaces

## Why this matters

As programs grow, you'll want code that works with many kinds of thing: send a notification by email *or* SMS, store data in SQLite *or* in memory for tests, export to CSV *or* JSON. There are two main tools for this. **Inheritance** builds new classes on top of old ones; **composition** builds objects out of other objects. Choosing well keeps code easy to change. Choosing badly gives you deep class trees where touching one class breaks five others, one of the most common design problems in real codebases.

## Inheritance: "is a"

**Inheritance** lets a new class (the **subclass** or **child**) reuse everything from an existing class (the **superclass**, **base class** or **parent**) and then add or change things:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} makes a sound: {self.sound()}"

    def sound(self):
        return "..."


class Dog(Animal):          # Dog inherits from Animal
    def sound(self):        # override: replace the parent's version
        return "Woof"


class Cat(Animal):
    def sound(self):
        return "Meow"


for pet in [Dog("Rex"), Cat("Tom")]:
    print(pet.describe())
# Rex makes a sound: Woof
# Tom makes a sound: Meow
```

`Dog` didn't define `__init__` or `describe`; it got them from `Animal`. It **overrode** `sound`, providing its own version. When `describe` calls `self.sound()`, Python looks for `sound` on the actual object first (a `Dog`), then walks up to the parent. This is **polymorphism**: one call (`pet.describe()`) that does the right thing for each kind of object.

## `super()`: calling the parent

When a child needs its own `__init__` but still wants the parent's setup, it calls the parent's version with `super()`:

```python
class Animal:
    def __init__(self, name):
        self.name = name


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)      # let Animal set self.name
        self.breed = breed          # then add Dog's own attribute


rex = Dog("Rex", "collie")
print(rex.name, rex.breed)   # Rex collie
```

Forget the `super().__init__(name)` line and `Animal.__init__` never runs, so `rex.name` doesn't exist:

```python
rex.name
# AttributeError: 'Dog' object has no attribute 'name'
```

If you see that error on an attribute you *know* the parent sets, check for a missing `super().__init__()`.

## When inheritance goes wrong

Inheritance says "a Dog **is a** kind of Animal: anything you can do with an Animal, you can do with a Dog". That promise is the whole contract. Break it and code that worked with the parent breaks with the child.

The classic example is squares and rectangles. Geometry says a square is a rectangle, so this looks reasonable:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def set_width(self, width):     # a square must stay square...
        self.width = width
        self.height = width
```

Now someone writes a function for rectangles:

```python
def double_width(rect):
    rect.set_width(rect.width * 2)
    return rect.area()

print(double_width(Rectangle(3, 3)))   # 18
print(double_width(Square(3)))         # 36   surprise!
```

A rectangle promises that changing the width leaves the height alone. A square can't keep that promise. The rule this breaks has a name, the **Liskov substitution principle**: a child must be usable anywhere the parent is, without surprises. "Is a" in everyday speech isn't the same as "is a" in code. The code meaning is "behaves like, in every way the parent promises".

Deep hierarchies make this worse. `Shape → Polygon → Rectangle → Square → ColouredSquare`: to understand one method you read five classes, and a change near the top ripples down through all of them.

## Composition: "has a"

**Composition** means an object holds other objects and delegates work to them, instead of inheriting from them:

```python
class Engine:
    def start(self):
        return "vroom"


class Car:
    def __init__(self):
        self.engine = Engine()       # a Car HAS an Engine

    def start(self):
        return self.engine.start()   # delegate


print(Car().start())   # vroom
```

A car isn't a kind of engine, so inheritance would be wrong here. With composition you can swap parts, too: give `Car.__init__` an `engine` parameter and you can build a car with an `ElectricEngine`, or a `FakeEngine` in tests.

Here's the square fixed with composition. It *uses* a rectangle without promising to *be* one:

```python
class Square:
    def __init__(self, side):
        self._rect = Rectangle(side, side)

    def resize(self, side):
        self._rect.width = side
        self._rect.height = side

    def area(self):
        return self._rect.area()


sq = Square(3)
sq.resize(5)
print(sq.area())   # 25
```

A `Square` has no `set_width`, so nobody can stretch it into a non-square, and `double_width(Square(3))` now fails loudly with `AttributeError` instead of quietly returning a wrong answer.

The guideline used across the industry is **"favour composition over inheritance"**. Use inheritance for a true, promise-keeping "is a" relationship, usually only one level deep. Use composition for "has a" and "uses a", which is most of the time.

> **Try it:** for each pair, decide "is a" or "has a": Car/Wheel, Manager/Employee, Library/Book, Square/Shape, Order/OrderLine, Logger/File.

## Duck typing

Python doesn't need a shared parent class for polymorphism. If an object has the method you call, it works:

```python
class EmailNotifier:
    def send(self, to, message):
        return f"email to {to}: {message}"


class SMSNotifier:
    def send(self, to, message):
        return f"sms to {to}: {message}"


def notify(notifier, to, message):
    return notifier.send(to, message)


print(notify(EmailNotifier(), "ada@example.com", "Hi"))   # email to ada@example.com: Hi
print(notify(SMSNotifier(), "+15550100", "Hi"))           # sms to +15550100: Hi
```

`notify` doesn't care what class it gets, only that it has `send`. This is **duck typing**: "if it walks like a duck and quacks like a duck, it's a duck". It's why Python code is so flexible, and it's what makes testing easy: hand `notify` a fake object that records messages and you can test it without sending a real email.

## Interfaces: writing the promise down

Duck typing has one weakness: the expected shape lives only in your head. An **interface** writes it down: "anything used here must have these methods". Python has two ways.

**`typing.Protocol`** describes a shape. Classes match it just by having the right methods, with no inheritance needed. That's duck typing with documentation:

```python
from typing import Protocol


class Notifier(Protocol):
    def send(self, to: str, message: str) -> str: ...


def notify(notifier: Notifier, to: str, message: str) -> str:
    return notifier.send(to, message)
```

The `...` (the Ellipsis) means "no body here; this only describes the shape". `EmailNotifier` and `SMSNotifier` above already match `Notifier` without changing a line. A type checker (see the lesson "Type hints") will now warn you if you pass something without a matching `send`.

**`abc.ABC`** (abstract base class) is the stricter, inheritance-based option. Subclasses must inherit from it and implement every `@abstractmethod`, or they can't be created:

```python
from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def export(self, rows: list[dict]) -> str: ...


class CSVExporter(Exporter):
    pass                         # forgot to implement export


CSVExporter()
# TypeError: Can't instantiate abstract class CSVExporter without an implementation for abstract method 'export'
```

Which to use? Prefer `Protocol` when you're describing what *your function needs* from its arguments, especially for things you'll fake in tests. Use `ABC` when you're building a family of classes that share real code in the base class and you want a missing method caught the moment someone tries to create the object.

## Prefer functions until you need a class

One last guideline: not everything needs a class. A class that has one method and an `__init__` that only stores its arguments is usually a function in disguise:

```python
class GreetingMaker:
    def __init__(self, name):
        self.name = name

    def make(self):
        return f"Hello, {self.name}"

# simpler:
def make_greeting(name):
    return f"Hello, {name}"
```

Reach for a class when you have state that changes over time, rules to protect, or several kinds of object that share an interface. Otherwise, a function is easier to read, test and reuse.

You may meet the acronym **SOLID**, a set of five design principles (Liskov substitution is the "L"). They're worth knowing by name, but don't treat them as laws. The habits in this lesson (shallow inheritance, composition, small interfaces) cover what matters for now.

## Common mistakes

**Inheriting just to reuse code.** If the child doesn't truly keep every promise of the parent, use composition. "I want those three methods" isn't a reason to inherit.

**Forgetting `super().__init__()`.** Symptoms: `AttributeError` for attributes the parent should have set.

**Overriding with a different signature.** If the parent's `send(to, message)` becomes `send(message)` in the child, every caller written for the parent breaks with `TypeError: ... takes 2 positional arguments but 3 were given`.

**Instantiating an ABC.** `TypeError: Can't instantiate abstract class ...` means a subclass is missing one of the abstract methods; the message names it.

**Building a hierarchy up front.** Don't design `BaseNotifier → AbstractChannelNotifier → EmailNotifier` before you have a second notifier. Write the concrete class first; extract an interface when a second one arrives.

## Recap

- Inheritance means "is a, keeping every promise". Use it sparingly and shallowly; call `super().__init__()` when you override `__init__`.
- The square/rectangle problem shows how inheritance breaks when a child can't keep the parent's promises (Liskov substitution).
- Composition, "has a", builds objects from parts and delegates to them. Favour it.
- Duck typing: any object with the right methods works. `Protocol` documents that shape; `ABC` enforces it through inheritance.
- Start with functions; add classes and interfaces when real needs show up.
