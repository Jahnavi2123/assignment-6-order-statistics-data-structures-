from dataclasses import dataclass
from typing import Any, Iterator, Optional


@dataclass
class Node:
    """
    One linked-list node containing a value and a reference to the
    next node in the sequence.
    """

    value: Any
    next: Optional["Node"] = None


class SinglyLinkedList:
    """
    A singly linked list with head and tail references.
    """

    def __init__(self) -> None:
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self._head

        while current is not None:
            yield current.value
            current = current.next

    def __str__(self) -> str:
        return " -> ".join(str(value) for value in self)

    def is_empty(self) -> bool:
        return self._head is None

    def insert_front(self, value: Any) -> None:
        new_node = Node(value, self._head)
        self._head = new_node

        # Inserting into an empty list creates both the first and last node.
        if self._tail is None:
            self._tail = new_node

        self._size += 1

    def insert_end(self, value: Any) -> None:
        new_node = Node(value)

        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            # Maintaining a tail reference avoids traversing the full list
            # whenever a new value is appended.
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1

    def insert_at(self, index: int, value: Any) -> None:
        if index < 0 or index > self._size:
            raise IndexError("Insertion index is out of range.")

        if index == 0:
            self.insert_front(value)
            return

        if index == self._size:
            self.insert_end(value)
            return

        previous = self._node_at(index - 1)
        previous.next = Node(value, previous.next)
        self._size += 1

    def delete_front(self) -> Any:
        if self._head is None:
            raise IndexError("Cannot delete from an empty linked list.")

        removed = self._head
        self._head = removed.next
        self._size -= 1

        if self._head is None:
            self._tail = None

        return removed.value

    def delete_value(self, value: Any) -> bool:
        previous: Optional[Node] = None
        current = self._head

        while current is not None:
            if current.value == value:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next

                if current is self._tail:
                    self._tail = previous

                self._size -= 1

                if self._size == 0:
                    self._head = None
                    self._tail = None

                return True

            previous = current
            current = current.next

        return False

    def delete_at(self, index: int) -> Any:
        if index < 0 or index >= self._size:
            raise IndexError("Deletion index is out of range.")

        if index == 0:
            return self.delete_front()

        previous = self._node_at(index - 1)
        removed = previous.next

        if removed is None:
            raise RuntimeError("Linked-list structure is inconsistent.")

        previous.next = removed.next

        if removed is self._tail:
            self._tail = previous

        self._size -= 1
        return removed.value

    def search(self, value: Any) -> int:
        current = self._head
        index = 0

        while current is not None:
            if current.value == value:
                return index

            current = current.next
            index += 1

        return -1

    def access(self, index: int) -> Any:
        return self._node_at(index).value

    def _node_at(self, index: int) -> Node:
        if index < 0 or index >= self._size:
            raise IndexError("Linked-list index is out of range.")

        current = self._head

        for _ in range(index):
            if current is None:
                raise RuntimeError("Linked-list structure is inconsistent.")

            current = current.next

        if current is None:
            raise RuntimeError("Linked-list structure is inconsistent.")

        return current

    def to_list(self) -> list[Any]:
        return list(self)


if __name__ == "__main__":
    linked_list = SinglyLinkedList()

    linked_list.insert_end(10)
    linked_list.insert_end(20)
    linked_list.insert_front(5)
    linked_list.insert_at(2, 15)

    print("List:", linked_list)
    print("Deleted:", linked_list.delete_at(1))
    print("Updated:", linked_list)