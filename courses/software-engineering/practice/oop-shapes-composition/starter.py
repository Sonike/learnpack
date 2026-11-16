# The broken version. Rewrite it so Square uses a Rectangle instead of inheriting from it.


class Shape:
    def area(self) -> float:
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def set_width(self, width: float) -> None:
        self.width = width

    def set_height(self, height: float) -> None:
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side: float):
        super().__init__(side, side)

    def set_width(self, width: float) -> None:  # breaks Rectangle's promise
        self.width = width
        self.height = width

    def set_height(self, height: float) -> None:
        self.width = height
        self.height = height


def total_area(shapes) -> float:
    # TODO
    return 0


# TODO: give Rectangle a resize(width, height) and Square a resize(side) and a side property,
#       validate sizes, and make Square hold a Rectangle (composition) instead of inheriting.


if __name__ == "__main__":
    sq = Square(3)
    sq.set_width(sq.width * 2)
    print("stretched square area:", sq.area(), "(a rectangle would give 18)")
