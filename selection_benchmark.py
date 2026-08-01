import random
import statistics
import time
from typing import Callable, Dict, List

from deterministic_selection import deterministic_select
from randomized_selection import randomized_select


SelectionFunction = Callable[[List[int], int], int]


def measure_time(
    algorithm: SelectionFunction,
    values: List[int],
    k: int,
    trials: int = 7,
) -> float:
    """
    Measure the median execution time across several trials.

    Median timing reduces the effect of one unusually slow execution
    caused by background processes or temporary interpreter activity.
    """

    expected = sorted(values)[k - 1]
    execution_times = []

    for _ in range(trials):
        test_data = values.copy()

        start = time.perf_counter()
        result = algorithm(test_data, k)
        elapsed = time.perf_counter() - start

        # A benchmark result is useful only if the algorithm is correct.
        if result != expected:
            raise ValueError(
                f"{algorithm.__name__} returned {result}, "
                f"but the expected value was {expected}."
            )

        execution_times.append(elapsed)

    return statistics.median(execution_times)


def create_datasets(size: int) -> Dict[str, List[int]]:
    """
    Build input distributions that exercise different algorithm behavior.
    """

    return {
        "Random": [
            random.randint(0, size * 10)
            for _ in range(size)
        ],
        "Sorted": list(range(size)),
        "Reverse": list(range(size, 0, -1)),
        "Repeated": [
            random.randint(1, 10)
            for _ in range(size)
        ],
    }


def run_benchmarks() -> None:
    random.seed(42)

    sizes = [100, 500, 1000, 2000, 5000]

    print(
        f"{'Size':<8}"
        f"{'Distribution':<15}"
        f"{'Deterministic':<18}"
        f"{'Randomized':<18}"
    )

    for size in sizes:
        datasets = create_datasets(size)

        for distribution, values in datasets.items():
            # Selecting the median gives both algorithms a meaningful
            # order statistic that is not always near an array boundary.
            k = (size + 1) // 2

            deterministic_time = measure_time(
                deterministic_select,
                values,
                k,
            )

            randomized_time = measure_time(
                randomized_select,
                values,
                k,
            )

            print(
                f"{size:<8}"
                f"{distribution:<15}"
                f"{deterministic_time:<18.6f}"
                f"{randomized_time:<18.6f}"
            )


if __name__ == "__main__":
    run_benchmarks()