import math


class Fraction:
    def __init__(self, numerator: int, denominator: int):
        if denominator == 0:
            raise ZeroDivisionError("denominator cannot be 0")
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        common = math.gcd(numerator, denominator)
        self.numerator = numerator // common
        self.denominator = denominator // common

    def __add__(self, other: "Fraction") -> "Fraction":
        return Fraction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        return (self.numerator, self.denominator) == (other.numerator, other.denominator)

    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"


if __name__ == "__main__":
    print(Fraction(2, 4))
    print(Fraction(1, 2) + Fraction(1, 3))
