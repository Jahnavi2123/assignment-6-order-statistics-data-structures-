from typing import Any, Iterator


class DynamicArray:
    """
    A simplified dynamic array implemented without using list append
    as the primary storage mechanism.
    """

    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity < 1:
            raise ValueError("Initial capacity must be at least one.")

        self._capacity = initial_capacity
        self._size = 0

        # A fixed-size Python list represents the allocated block of space.
        self._data = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        for index in range(self._size):
            yield self._data[index]

    def __str__(self) -> str:
        return str(list(self))

    def _validate_access_index(self, index: int) -> None:
        if index < 0 or index >= self._size:
            raise IndexError("Array index is out of range.")

    def _validate_insert_index(self, index: int) -> None:
        if index < 0 or index > self._size:
            raise IndexError("Insertion index is out of range.")

    def _resize(self, new_capacity: int) -> None:
        """
        Move existing values into a larger or smaller storage block.

        Resizing costs O(n), but it happens infrequently. As a result,
        repeated append operations remain O(1) amortized.
        """

        resized_data = [None] * new_capacity

        for index in range(self._size):
            resized_data[index] = self._data[index]

        self._data = resized_data
        self._capacity = new_capacity

    def access(self, index: int) -> Any:
        self._validate_access_index(index)
        return self._data[index]

    def update(self, index: int, value: Any) -> None:
        self._validate_access_index(index)
        self._data[index] = value

    def append(self, value: Any) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        self._data[self._size] = value
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        self._validate_insert_index(index)

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        # Values at and after the insertion point must move one position
        # to the right to create an empty slot.
        for current in range(self._size, index, -1):
            self._data[current] = self._data[current - 1]

        self._data[index] = value
        self._size += 1

    def delete(self, index: int) -> Any:
        self._validate_access_index(index)

        removed = self._data[index]

        # Closing the gap requires all later values to shift left.
        for current in range(index, self._size - 1):
            self._data[current] = self._data[current + 1]

        self._size -= 1
        self._data[self._size] = None

        # Shrinking avoids retaining a large block after many deletions.
        # Capacity is never reduced below the original minimum of four.
        if (
            self._capacity > 4
            and self._size <= self._capacity // 4
        ):
            self._resize(max(4, self._capacity // 2))

        return removed

    def search(self, value: Any) -> int:
        for index in range(self._size):
            if self._data[index] == value:
                return index

        return -1


if __name__ == "__main__":
    array = DynamicArray()

    array.append(10)
    array.append(20)
    array.insert(1, 15)

    print("Array:", array)
    print("Access index 1:", array.access(1))
    print("Deleted:", array.delete(0))
    print("Updated array:", array)