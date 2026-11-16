# Split a file name into stem and extension

A file **extension** is just the end of the name, after the last dot: `report.pdf` has the extension `.pdf`. The rest is called the **stem**. Write the split yourself.

```python
def split_name(filename: str) -> tuple[str, str]: ...
```

- `filename` is a file name with no folders in it, such as `"notes.txt"`.
- Return `(stem, extension)`. The extension includes the dot.
- Only the **last** dot counts: `"archive.tar.gz"` → `("archive.tar", ".gz")`.
- No dot means no extension: `"README"` → `("README", "")`.
- A name that **starts** with a dot and has no other dot is a hidden file, not an extension: `".bashrc"` → `(".bashrc", "")`.

These are the same rules as Python's `pathlib.PurePosixPath(name).stem` and `.suffix`, which the tests use to check you. Write it with string methods (`rfind` is handy), not `pathlib`.

## Example

```python
split_name("photo.jpg")       # ("photo", ".jpg")
split_name("archive.tar.gz")  # ("archive.tar", ".gz")
split_name(".bashrc")         # (".bashrc", "")
split_name("Makefile")        # ("Makefile", "")
```
