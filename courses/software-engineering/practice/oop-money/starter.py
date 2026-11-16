from dataclasses import dataclass


# TODO: make it frozen
@dataclass
class Money:
    amount_cents: int
    currency: str

    def __add__(self, other: "Money") -> "Money":
        # TODO: refuse mixed currencies with ValueError, else return a new Money
        return self

    def __str__(self) -> str:
        # TODO: "12.50 USD", "-2.50 EUR", "0.05 USD"
        return "?"


if __name__ == "__main__":
    price = Money(1250, "USD")
    print(price + Money(100, "USD"))  # 13.50 USD
    print(Money(-250, "EUR"))         # -2.50 EUR
    try:
        price + Money(500, "EUR")
    except ValueError as e:
        print("Refused:", e)
