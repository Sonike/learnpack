# Fix a broken hierarchy with composition

The starter has a classic inheritance trap. `Square` inherits from `Rectangle`, because "a square *is a* rectangle" sounds right. But a rectangle promises that you can change its width without changing its height. A square can't keep that promise, so code written for rectangles breaks when it's handed a square:

```python
def stretch(rect):
    rect.set_width(rect.width * 2)   # "double the width, so double the area"

sq = Square(3)
stretch(sq)
sq.area()    # 36, not 18: the height changed too
```

Breaking a parent's promise like this is called a **Liskov substitution** violation (LSP). Rewrite the classes so that:

```python
class Rectangle:
    def __init__(self, width: float, height: float): ...
    def area(self) -> float: ...
    def resize(self, width: float, height: float) -> None: ...

class Square:
    def __init__(self, side: float): ...
    def area(self) -> float: ...
    def resize(self, side: float) -> None: ...

def total_area(shapes) -> float: ...
```

- `Square` must **not** inherit from `Rectangle`. Use **composition** instead: a `Square` keeps a `Rectangle` inside it (for example `self._rect = Rectangle(side, side)`) and passes `area()` on to it.
- `Rectangle` has `width` and `height` attributes. `Square` has a `side` property that reads from its inner rectangle.
- `Square.resize(side)` takes **one** number, so a square can't become non-square.
- Width, height and side must be positive: zero or negative raises `ValueError` (in `__init__` and in `resize`).
- `total_area(shapes)` adds up `shape.area()` for any objects with an `area()` method (duck typing).

## Example

```python
sq = Square(3)
sq.resize(5)
sq.area(), sq.side                                # (25, 5)
total_area([Rectangle(2, 3), Square(2)])          # 10
issubclass(Square, Rectangle)                     # False
```
