from solution import Rectangle, Square, total_area


def test_square_does_not_inherit_from_rectangle():
    assert not issubclass(Square, Rectangle), "Square should hold a Rectangle (composition), not inherit from it"


def test_rectangle_area_and_resize():
    rect = Rectangle(2, 3)
    assert rect.area() == 6, f"expected 6, got {rect.area()!r}"
    rect.resize(4, 3)
    assert (rect.width, rect.height, rect.area()) == (4, 3, 12), f"got {(rect.width, rect.height, rect.area())!r}"


def test_square_stays_square_after_resize():
    sq = Square(3)
    assert sq.area() == 9, f"expected 9, got {sq.area()!r}"
    sq.resize(5)
    got = (sq.side, sq.area())
    assert got == (5, 25), f"expected (5, 25), got {got!r}"


def test_total_area_works_for_mixed_shapes():
    got = total_area([Rectangle(2, 3), Square(2)])
    assert got == 10, f"expected 10, got {got!r}"
    assert total_area([]) == 0, "the total area of no shapes is 0"


def test_rejects_non_positive_sizes():
    attempts = [lambda: Rectangle(0, 3), lambda: Square(-1), lambda: Square(2).resize(0), lambda: Rectangle(1, 1).resize(1, -2)]
    for i, attempt in enumerate(attempts):
        try:
            attempt()
        except ValueError:
            continue
        raise AssertionError(f"attempt {i + 1} used a zero or negative size and should raise ValueError")
