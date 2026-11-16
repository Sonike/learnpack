import re
import unicodedata


def slugify(title: str) -> str:
    """Turn a title into a lowercase, dash-separated, ASCII-only slug."""
    plain = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


if __name__ == "__main__":
    print(slugify("Café au Lait: 10 Tips!"))
