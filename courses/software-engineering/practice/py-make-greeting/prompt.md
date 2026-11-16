# Keyword-only arguments

Some options are clearer when the caller has to name them. Compare `make_greeting("Sam", True)` (true *what*?) with `make_greeting("Sam", formal=True)`. A bare `*` in the parameter list makes everything after it **keyword-only**: it can only be passed by name.

```python
def make_greeting(name: str, *, formal: bool = False, title: str | None = None) -> str: ...
```

- `name`: the person's name.
- `formal` (keyword-only, default `False`): informal greetings are `"Hi, <who>!"`; formal ones are `"Good day, <who>."`.
- `title` (keyword-only, default `None`): if given, put it before the name with a space, e.g. `title="Dr"` makes `<who>` = `"Dr Sam"`. `None` means "no title".

Calling `make_greeting("Sam", True)` must fail with a `TypeError`. You get that for free once the `*` is in the right place.

## Example

```python
make_greeting("Sam")                            # "Hi, Sam!"
make_greeting("Sam", formal=True)               # "Good day, Sam."
make_greeting("Okafor", formal=True, title="Dr")  # "Good day, Dr Okafor."
make_greeting("Sam", title="Captain")           # "Hi, Captain Sam!"
```
