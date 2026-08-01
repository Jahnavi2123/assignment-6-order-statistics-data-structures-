from typing import List


def deterministic_select(values: List[int], k: int) -> int:
    """
    Return the kth smallest value using the Median of Medians algorithm.

    The value of k is one-based:
        k = 1 returns the smallest value.
        k = len(values) returns the largest value.

    A copy of the input list is used so that the caller's original
    data is not changed.
    """

    if not values:
        raise ValueError("Cannot select an element from an empty list.")

    if k < 1 or k > len(values):
        raise IndexError(
            f"k must be between 1 and {len(values)}, but received {k}."
        )

    # Internally, zero-based indexing is easier to use. For example,
    # the first smallest element has target index zero.
    target_index = k - 1

    return _select(values.copy(), target_index)


def _select(values: List[int], target_index: int) -> int:
    """
    Select the element at target_index from the sorted order of values.

    This function does not fully sort the input. It repeatedly removes
    the part of the problem that cannot contain the requested element.
    """

    # For a small group, directly sorting is simple and inexpensive.
    # The constant group size prevents this step from changing the
    # overall linear-time complexity.
    if len(values) <= 5:
        return sorted(values)[target_index]

    pivot = _median_of_medians(values)

    # Three-way partitioning is important because duplicate pivot values
    # should be grouped together instead of being processed recursively.
    lower = []
    equal = []
    higher = []

    for value in values:
        if value < pivot:
            lower.append(value)
        elif value > pivot:
            higher.append(value)
        else:
            equal.append(value)

    # If the requested position lies in the lower partition, the same
    # target index can be used because no earlier elements were removed.
    if target_index < len(lower):
        return _select(lower, target_index)

    # All values in the equal partition are identical to the pivot.
    # Therefore, any target located in this range has value pivot.
    if target_index < len(lower) + len(equal):
        return pivot

    # The lower and equal partitions are removed before searching the
    # higher partition. The target index must therefore be adjusted.
    adjusted_index = target_index - len(lower) - len(equal)

    return _select(higher, adjusted_index)


def _median_of_medians(values: List[int]) -> int:
    """
    Choose a pivot that guarantees sufficient progress in each recursion.

    Values are divided into groups of at most five. The median of each
    group is collected, and the median of those medians becomes the pivot.
    """

    medians = []

    # Groups of five provide the balance needed for the worst-case
    # linear-time guarantee while keeping each small sort inexpensive.
    for start in range(0, len(values), 5):
        group = values[start:start + 5]
        group.sort()

        # The final group may contain fewer than five elements, but its
        # middle value can still be used as that group's representative.
        median = group[len(group) // 2]
        medians.append(median)

    # When only one median remains, it is the chosen pivot.
    if len(medians) == 1:
        return medians[0]

    # Recursively select the median of the collected medians.
    median_position = len(medians) // 2

    return _select(medians, median_position)


if __name__ == "__main__":
    test_cases = [
        ([7, 2, 9, 1, 5], 3),
        ([4, 4, 2, 1, 4, 3], 4),
        ([-5, 8, 0, -2, 10], 1),
        ([10], 1),
        ([9, 8, 7, 6, 5, 4], 6),
    ]

    for numbers, order in test_cases:
        result = deterministic_select(numbers, order)
        expected = sorted(numbers)[order - 1]

        print(
            f"Input: {numbers}, k={order}, "
            f"result={result}, expected={expected}"
        )

        assert result == expected

    print("All deterministic selection tests passed.")