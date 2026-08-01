import random
from typing import List, Tuple


def randomized_select(values: List[int], k: int) -> int:
    """
    Return the kth smallest value using Randomized Quickselect.

    The public interface uses one-based k values. The implementation
    works on a copy so the original list is not modified.
    """

    if not values:
        raise ValueError("Cannot select an element from an empty list.")

    if k < 1 or k > len(values):
        raise IndexError(
            f"k must be between 1 and {len(values)}, but received {k}."
        )

    data = values.copy()
    target_index = k - 1

    return _quickselect(data, 0, len(data) - 1, target_index)


def _quickselect(
    values: List[int],
    low: int,
    high: int,
    target_index: int,
) -> int:
    """
    Iteratively narrow the active portion of the array.

    An iterative loop is used instead of ordinary recursion so that the
    implementation does not create an unnecessary Python stack frame for
    every partition.
    """

    while low <= high:
        if low == high:
            return values[low]

        # Selecting the pivot uniformly from the active subarray prevents
        # performance from being tied to the original order of the input.
        pivot_index = random.randint(low, high)
        pivot_value = values[pivot_index]

        equal_start, equal_end = _three_way_partition(
            values,
            low,
            high,
            pivot_value,
        )

        if target_index < equal_start:
            # The desired element must be in the section smaller than
            # the pivot, so the upper boundary is moved left.
            high = equal_start - 1
        elif target_index > equal_end:
            # The desired element must be in the section greater than
            # the pivot, so the lower boundary is moved right.
            low = equal_end + 1
        else:
            # Every value between equal_start and equal_end is the pivot.
            return values[target_index]

    raise RuntimeError("Selection failed because the search range was invalid.")


def _three_way_partition(
    values: List[int],
    low: int,
    high: int,
    pivot: int,
) -> Tuple[int, int]:
    """
    Partition values[low:high + 1] into three sections:

        values smaller than pivot
        values equal to pivot
        values greater than pivot

    The returned indices describe the first and last positions occupied
    by values equal to the pivot.
    """

    smaller = low
    current = low
    greater = high

    while current <= greater:
        if values[current] < pivot:
            values[smaller], values[current] = (
                values[current],
                values[smaller],
            )

            smaller += 1
            current += 1

        elif values[current] > pivot:
            values[current], values[greater] = (
                values[greater],
                values[current],
            )

            # The replacement value at current has not been examined yet.
            # Therefore, current must remain in place for another iteration.
            greater -= 1

        else:
            current += 1

    return smaller, greater


if __name__ == "__main__":
    random.seed(42)

    test_cases = [
        ([7, 2, 9, 1, 5], 3),
        ([4, 4, 2, 1, 4, 3], 4),
        ([-5, 8, 0, -2, 10], 1),
        ([10], 1),
        ([9, 8, 7, 6, 5, 4], 6),
    ]

    for numbers, order in test_cases:
        result = randomized_select(numbers, order)
        expected = sorted(numbers)[order - 1]

        print(
            f"Input: {numbers}, k={order}, "
            f"result={result}, expected={expected}"
        )

        assert result == expected

    print("All randomized selection tests passed.")