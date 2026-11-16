def _check_positive(*sizes: float) -> None:
    if any(size <= 0 for size in sizes):
        raise ValueError("sizes must be positive")


class Rectangle:
    def __init__(self, width: float, height: float):
        _check_positive(width, height)
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def resize(self, width: float, height: float) -> None:
        _check_positive(width, height)
        self.width = width
        self.height = height


class Square:
    def __init__(self, side: float):
        self._rect = Rectangle(side, side)

    @property
    def side(self) -> float:
        return self._rect.width

    def area(self) -> float:
        return self._rect.area()

    def resize(self, side: float) -> None:
        self._rect.resize(side, side)


def total_area(shapes) -> float:
    return sum(shape.area() for shape in shapes)


if __name__ == "__main__":
    sq = Square(3)
    sq.resize(5)
    print(sq.area(), total_area([Rectangle(2, 3), Square(2)]))
