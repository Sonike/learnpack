# Library system

Build the core of a small lending library as plain Python: the objects, the rules and nothing else. No database, no web pages, no menus. It's a **domain model**: code that captures how a real-world business works. Every later section builds on this kind of code, and the next project (in the testing section) adds a full test suite to this same repository, so design it to be tested.

## What you're building

A library lends books to members. Your code should be able to:

- add books and members;
- lend a book to a member, and take it back;
- refuse loans that break the rules;
- work out late fees;
- notify members when a book is due or overdue.

Everything happens through Python objects and functions. A short `demo.py` that runs a scripted scenario and prints what happens is enough to show it working.

## The rules

Pick sensible numbers and keep them as named constants. Here's a starting set:

- A member can have at most **3** books on loan at once.
- A loan lasts **14 days**.
- A book that's already on loan can't be lent again until it's returned.
- A late return costs **25 cents per day late**, capped at **10.00** per loan.
- A member who owes more than **5.00** in fees can't borrow until they pay.

## Design requirements

- **Dataclasses and enums.** Model `Book`, `Member` and `Loan` as dataclasses. Use an `Enum` for anything with a fixed set of values, such as a book's status (available, on loan, lost) or a member's type. Money is an `int` in cents, or a small frozen `Money` dataclass.
- **An injected clock.** Nothing calls `datetime.now()` or `date.today()` deep in the logic. Functions that need the date take a `today` argument, or the library takes a clock function in its constructor. This is what will make the next project's tests easy.
- **Composition over inheritance.** A `Library` *has* books, members and loans. If you're tempted to write a class hierarchy, write down why in your design notes first.
- **One `Protocol` for notifications.** Define a `Notifier` protocol with one method (for example `send(member, message)`). Write a `ConsoleNotifier` that prints and an `InMemoryNotifier` that records messages in a list. The library receives a notifier and doesn't care which one.
- **Type hints everywhere,** and a type checker (mypy or pyright) that passes with no errors.
- **Clean code.** Ruff format and ruff check pass. No function is longer than 25 lines. No magic numbers. Pure logic (fees, can-borrow checks) is kept separate from printing.
- **Errors that explain themselves.** Breaking a rule raises a clear exception (a `ValueError`, or your own `LoanError(Exception)`) with a message a person can read, like `"Ada already has 3 books on loan"`.

## Suggested steps

1. Write the dataclasses and enums first, with no behaviour. Create a few in the REPL.
2. Write the pure rule functions: `can_borrow(member, loans, today)`, `late_fee(loan, returned_on)`. Check them with a few `assert`s in a scratch file.
3. Write the `Library` class that wires them together: `lend(book_id, member_id, today)`, `return_book(book_id, today)`, `send_reminders(today)`.
4. Add the notifier protocol and the two implementations.
5. Run ruff and your type checker, fix everything, and split any function over 25 lines.
6. Write `demo.py` and the README.

## README

Include: what the project is, how to run the demo, and a **Design notes** section explaining at least two decisions you made and what you considered instead. For example: why `Loan` is its own class instead of a list on `Member`, why you injected the clock, or how you modelled money.

> **On AI tools:** it's fine to ask an assistant to explain a type-checker error or to review your design notes. Write the classes and rules yourself; this project is where object design clicks, and only if you do the designing.
