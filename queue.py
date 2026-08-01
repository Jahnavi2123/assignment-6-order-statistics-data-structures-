from typing import Any, List


class CircularQueue:
    """
    A first-in, first-out queue backed by a circular array.

    A circular representation prevents dequeue from shifting every
    remaining element, allowing expected O(1) queue operations.
    """

    def __init__(self, initial_capacity: int = 4) -> None:
        if initial_capacity < 1:
            raise ValueError("Initial capacity must be at least one.")

        self._capacity = initial_capacity
        self._data: List[Any] = [None] * initial_capacity
        self._front = 0
        self._size = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def _resize(self, new_capacity: int) -> None:
        resized = [None] * new_capacity

        # Values are copied in logical queue order rather than physical
        # array order because wrapping may split the queue into two parts.
        for offset in range(self._size):
            old_index = (self._front + offset) % self._capacity
            resized[offset] = self._data[old_index]

        self._data = resized
        self._capacity = new_capacity
        self._front = 0

    def enqueue(self, value: Any) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        rear = (self._front + self._size) % self._capacity
        self._data[rear] = value
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")

        value = self._data[self._front]
        self._data[self._front] = None

        # Modulo arithmetic wraps the front to index zero when it passes
        # the end of the allocated array.
        self._front = (self._front + 1) % self._capacity
        self._size -= 1

        return value

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("Cannot read the front of an empty queue.")

        return self._data[self._front]

    def to_list(self) -> List[Any]:
        return [
            self._data[(self._front + offset) % self._capacity]
            for offset in range(self._size)
        ]


if __name__ == "__main__":
    queue = CircularQueue()

    queue.enqueue("request-1")
    queue.enqueue("request-2")
    queue.enqueue("request-3")

    print("Front:", queue.front())

    while not queue.is_empty():
        print("Dequeued:", queue.dequeue())