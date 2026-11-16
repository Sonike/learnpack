# Transpose a grid

A list of lists is a handy way to store a grid (a spreadsheet, a game board, a matrix). **Transposing** turns rows into columns:

```
1 2 3        1 4
4 5 6   →    2 5
             3 6
```

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]: ...
```

- `matrix` is a list of rows; every row has the same length.
- Return a new list of lists where row `i` of the result is column `i` of `matrix`.
- An empty matrix `[]` returns `[]`.
- Don't change `matrix`.

Write it with two nested loops first. (Once it works, look up what `zip(*matrix)` does; it's a neat one-liner, but understand the loops first.)

## Example

```python
transpose([[1, 2, 3], [4, 5, 6]])   # [[1, 4], [2, 5], [3, 6]]
transpose([[7]])                    # [[7]]
transpose([])                       # []
```
