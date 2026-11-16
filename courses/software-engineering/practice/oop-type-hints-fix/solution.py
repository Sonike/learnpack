from collections.abc import Callable


def find_age(ages: dict[str, int], name: str) -> int | None:
    return ages.get(name)


def total_age(ages: dict[str, int], names: list[str]) -> int:
    total = 0
    for name in names:
        age = find_age(ages, name)
        if age is not None:
            total += age
    return total


def describe(name: str, age: int | None) -> str:
    if age is None:
        return f"{name}'s age is unknown"
    return f"{name} is {age}"


def apply_all(values: list[int], fn: Callable[[int], int]) -> list[int]:
    return [fn(v) for v in values]


if __name__ == "__main__":
    ages = {"Ada": 36, "Alan": 41}
    print(find_age(ages, "Grace"), total_age(ages, ["Ada", "Grace", "Alan"]), describe("Ada", 36))
