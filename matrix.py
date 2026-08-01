from typing import Any, Iterable, List


class Matrix:
    """
    A rectangular matrix with basic access and structural operations.
    """

    def __init__(self, rows: int, columns: int, default: Any = 0) -> None:
        if rows < 1 or columns < 1:
            raise ValueError("A matrix must have at least one row and column.")

        self._data = [
            [default for _ in range(columns)]
            for _ in range(rows)
        ]

    @property
    def rows(self) -> int:
        return len(self._data)

    @property
    def columns(self) -> int:
        return len(self._data[0])

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self._data)

    def _validate_position(self, row: int, column: int) -> None:
        if row < 0 or row >= self.rows:
            raise IndexError("Row index is out of range.")

        if column < 0 or column >= self.columns:
            raise IndexError("Column index is out of range.")

    def access(self, row: int, column: int) -> Any:
        self._validate_position(row, column)
        return self._data[row][column]

    def update(self, row: int, column: int, value: Any) -> None:
        self._validate_position(row, column)
        self._data[row][column] = value

    def insert_row(self, index: int, values: Iterable[Any]) -> None:
        row = list(values)

        if len(row) != self.columns:
            raise ValueError(
                f"New row must contain exactly {self.columns} values."
            )

        if index < 0 or index > self.rows:
            raise IndexError("Row insertion index is out of range.")

        self._data.insert(index, row)

    def delete_row(self, index: int) -> List[Any]:
        if self.rows == 1:
            raise ValueError("Cannot delete the matrix's only row.")

        if index < 0 or index >= self.rows:
            raise IndexError("Row deletion index is out of range.")

        return self._data.pop(index)

    def insert_column(
        self,
        index: int,
        values: Iterable[Any],
    ) -> None:
        column = list(values)

        if len(column) != self.rows:
            raise ValueError(
                f"New column must contain exactly {self.rows} values."
            )

        if index < 0 or index > self.columns:
            raise IndexError("Column insertion index is out of range.")

        # Each row receives one value at the same column position.
        for row_index, row in enumerate(self._data):
            row.insert(index, column[row_index])

    def delete_column(self, index: int) -> List[Any]:
        if self.columns == 1:
            raise ValueError("Cannot delete the matrix's only column.")

        if index < 0 or index >= self.columns:
            raise IndexError("Column deletion index is out of range.")

        removed = []

        for row in self._data:
            removed.append(row.pop(index))

        return removed

    def to_list(self) -> List[List[Any]]:
        # Return row copies so callers cannot alter internal storage
        # without going through the matrix operations.
        return [row.copy() for row in self._data]


if __name__ == "__main__":
    matrix = Matrix(2, 3)

    matrix.update(0, 1, 8)
    matrix.insert_row(2, [1, 2, 3])
    matrix.insert_column(0, [9, 8, 7])

    print(matrix)