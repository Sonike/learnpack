def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Return a new grid whose rows are the columns of matrix."""
    if not matrix:
        return []
    result = []
    for c in range(len(matrix[0])):
        column = []
        for row in matrix:
            column.append(row[c])
        result.append(column)
    return result


if __name__ == "__main__":
    print(transpose([[1, 2, 3], [4, 5, 6]]))   # [[1, 4], [2, 5], [3, 6]]
