import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a title into a lowercase, dash-separated, ASCII-only slug."""
    # TODO: 1. accents -> plain ASCII  2. lowercase  3. runs of other chars -> "-"  4. strip dashes
    return title


if __name__ == "__main__":
    for title in ["Hello World", "Café au Lait: 10 Tips!", "a -- b __ c", "!!!"]:
        print(repr(title), "->", repr(slugify(title)))
