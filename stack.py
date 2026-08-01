from typing import Any, List


class ArrayStack:
    """
    A last-in, first-out structure backed by a Python list.
    """

    def __init__(self) -> None:
        self._items: List[Any] = []

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def push(self, value: Any) -> None:
        # Appending at the end avoids shifting existing elements.
        self._items.append(value)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")

        return self._items.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")

        return self._items[-1]

    def to_list(self) -> List[Any]:
        return self._items.copy()


if __name__ == "__main__":
    stack = ArrayStack()

    stack.push("open file")
    stack.push("edit file")
    stack.push("save file")

    print("Top:", stack.peek())

    while not stack.is_empty():
        print("Popped:", stack.pop())