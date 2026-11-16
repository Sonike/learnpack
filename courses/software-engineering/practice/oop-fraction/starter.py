import math


class Fraction:
    def __init__(self, numerator: int, denominator: int):
        # TODO: raise ZeroDivisionError if denominator == 0
        # TODO: move the sign to the numerator, then reduce with math.gcd
        self.numerator = numerator
        self.denominator = denominator

    def __add__(self, other: "Fraction") -> "Fraction":
        # TODO: a/b + c/d = (a*d + c*b) / (b*d)
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        # TODO: compare numerators and denominators
        return False

    def __repr__(self) -> str:
        # TODO: Fraction(1, 2)
        return "Fraction(?)"


if __name__ == "__main__":
    print(Fraction(2, 4))                    # Fraction(1, 2)
    print(Fraction(1, 2) + Fraction(1, 3))   # Fraction(5, 6)
    print(Fraction(1, -2))                   # Fraction(-1, 2)
    print(Fraction(1, 2) == Fraction(3, 6))  # True
