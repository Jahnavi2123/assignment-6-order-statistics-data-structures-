import random

from deterministic_selection import deterministic_select
from dynamic_array import DynamicArray
from linked_list import SinglyLinkedList
from matrix import Matrix
from queue import CircularQueue
from randomized_selection import randomized_select
from stack import ArrayStack


def test_selection_algorithms() -> None:
    random.seed(42)

    cases = [
        [],
        [5],
        [3, 1, 2],
        [4, 4, 4, 4],
        [-5, 8, 0, -2, 10],
        list(range(20)),
        list(range(20, 0, -1)),
        [2, 1, 2, 3, 1, 2, 4],
    ]

    for values in cases:
        if not values:
            for algorithm in (
                deterministic_select,
                randomized_select,
            ):
                try:
                    algorithm(values, 1)
                    raise AssertionError(
                        "Empty input should raise ValueError."
                    )
                except ValueError:
                    pass

            continue

        original = values.copy()

        for k in range(1, len(values) + 1):
            expected = sorted(values)[k - 1]

            assert deterministic_select(values, k) == expected
            assert randomized_select(values, k) == expected

        # Both public functions promise not to alter the caller's list.
        assert values == original

    print("Selection algorithm tests passed.")


def test_dynamic_array() -> None:
    array = DynamicArray()

    array.append(10)
    array.append(20)
    array.insert(1, 15)

    assert list(array) == [10, 15, 20]
    assert array.access(1) == 15
    assert array.search(20) == 2

    array.update(1, 16)
    assert array.access(1) == 16
    assert array.delete(0) == 10
    assert list(array) == [16, 20]

    print("Dynamic array tests passed.")


def test_matrix() -> None:
    matrix = Matrix(2, 2)

    matrix.update(0, 1, 5)
    assert matrix.access(0, 1) == 5

    matrix.insert_row(2, [7, 8])
    matrix.insert_column(1, [1, 2, 3])

    assert matrix.to_list() == [
        [0, 1, 5],
        [0, 2, 0],
        [7, 3, 8],
    ]

    assert matrix.delete_column(1) == [1, 2, 3]
    assert matrix.delete_row(2) == [7, 8]

    print("Matrix tests passed.")


def test_stack() -> None:
    stack = ArrayStack()

    assert stack.is_empty()

    stack.push("A")
    stack.push("B")

    assert stack.peek() == "B"
    assert stack.pop() == "B"
    assert stack.pop() == "A"
    assert stack.is_empty()

    print("Stack tests passed.")


def test_queue() -> None:
    queue = CircularQueue(2)

    queue.enqueue("A")
    queue.enqueue("B")

    assert queue.dequeue() == "A"

    queue.enqueue("C")
    queue.enqueue("D")

    assert queue.to_list() == ["B", "C", "D"]
    assert queue.front() == "B"

    assert queue.dequeue() == "B"
    assert queue.dequeue() == "C"
    assert queue.dequeue() == "D"
    assert queue.is_empty()

    print("Queue tests passed.")


def test_linked_list() -> None:
    linked_list = SinglyLinkedList()

    linked_list.insert_end(10)
    linked_list.insert_end(20)
    linked_list.insert_front(5)
    linked_list.insert_at(2, 15)

    assert linked_list.to_list() == [5, 10, 15, 20]
    assert linked_list.search(15) == 2
    assert linked_list.access(3) == 20

    assert linked_list.delete_value(10)
    assert linked_list.delete_at(2) == 20
    assert linked_list.delete_front() == 5
    assert linked_list.to_list() == [15]

    print("Linked-list tests passed.")


def main() -> None:
    test_selection_algorithms()
    test_dynamic_array()
    test_matrix()
    test_stack()
    test_queue()
    test_linked_list()

    print("\nAll Assignment 6 tests passed successfully.")


if __name__ == "__main__":
    main()