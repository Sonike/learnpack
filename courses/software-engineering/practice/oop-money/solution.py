from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"cannot add {self.currency} and {other.currency}")
        return Money(self.amount_cents + other.amount_cents, self.currency)

    def __str__(self) -> str:
        sign = "-" if self.amount_cents < 0 else ""
        units, cents = divmod(abs(self.amount_cents), 100)
        return f"{sign}{units}.{cents:02d} {self.currency}"


if __name__ == "__main__":
    print(Money(1250, "USD") + Money(100, "USD"))
