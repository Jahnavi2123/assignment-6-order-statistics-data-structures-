# Assignment 6: Medians, Order Statistics, and Elementary Data Structures

## Introduction

Finding the median or another ranked value does not always require sorting an entire dataset. If an application needs only the fifth-smallest transaction, the median response time, or a percentile threshold, a selection algorithm can avoid some of the work performed by a complete sorting algorithm.

This assignment compares two approaches to selection. The deterministic implementation uses Median of Medians and guarantees linear running time in the worst case. The randomized implementation uses Quickselect and achieves linear running time in expectation. The second part of the assignment examines elementary data structures and shows how their storage models affect the cost of common operations.

# Part 1: Selection Algorithms

## Order Statistics

The kth order statistic is the value that would appear in position k if the input were sorted. For example, the first order statistic is the minimum, the final order statistic is the maximum, and the middle order statistic represents the median.

Both implementations use one-based values of k. This makes the public interface easier to understand because requesting k = 1 clearly means requesting the smallest value.

## Deterministic Selection Design

The deterministic implementation uses the Median of Medians strategy. The input is divided into groups of at most five values. Each group is sorted, and its median is collected. The algorithm then recursively selects the median of these medians and uses it as the partition pivot.

The purpose of this extra work is not to find the perfect median. Instead, it finds a pivot that is guaranteed not to be extremely close to either end of the sorted order. This guarantee ensures that every recursive call removes a meaningful fraction of the remaining input.

Three-way partitioning divides the data into values smaller than, equal to, and greater than the pivot. The equal section is especially useful for duplicate-heavy data because all copies of the pivot can be removed from further processing at the same time.

## Why Median of Medians Is Worst-Case O(n)

Groups of five are used because they provide a useful balance between pivot quality and grouping overhead. At least half of the group medians are greater than or equal to the median of medians. In each of those groups, at least three values are greater than or equal to that group median. A similar argument applies to values less than or equal to the pivot.

As a result, the recursive selection problem contains at most approximately 7n/10 values, excluding a small constant number of incomplete-group cases. The recurrence can be written as:

\[
T(n) \leq T(n/5) + T(7n/10) + O(n)
\]

The first recursive term selects the pivot from the group medians. The second term represents the largest possible remaining partition. The linear term covers grouping and partitioning.

Because the recursive subproblems together contain less than the full input by a fixed fraction, the recurrence solves to:

\[
T(n) = O(n)
\]

This guarantee applies even when the input is already sorted, reverse sorted, or arranged in an intentionally difficult order.

## Randomized Quickselect Design

Randomized Quickselect chooses a pivot uniformly from the active part of the array. It partitions the values and continues only in the section containing the requested order statistic.

Unlike Quicksort, Quickselect does not recursively process both partitions. Once the target is known to be on one side of the pivot, the other side is discarded. This difference is the main reason selection can run in expected linear time.

The implementation uses an iterative loop rather than one recursive call per partition. This avoids unnecessary stack growth and makes the implementation safer when an unlucky sequence of pivots produces several unbalanced partitions.

## Why Randomized Quickselect Is Expected O(n)

A single partition operation takes O(n) time for an input of size n. If the pivot creates reasonably balanced partitions, the next problem is significantly smaller. The expected work can be described informally as:

\[
T(n) = T(cn) + O(n)
\]

where c is a constant smaller than one for a sufficiently balanced partition.

The total work then resembles:

\[
n + cn + c^2n + c^3n + \cdots
\]

This is a decreasing geometric series whose sum is O(n). Although an individual pivot may be poor, random selection makes repeated poor pivots unlikely.

The worst case remains O(n²). It occurs when every chosen pivot is repeatedly the smallest or largest active value. Randomization does not make this impossible, but it makes the pattern unlikely and independent of the original data order.

## Duplicate Handling

Both algorithms use three-way partitioning. Values equal to the pivot form their own section. If the requested index lies in this section, the algorithm immediately returns the pivot.

This approach performs better than a two-way partition on data with many duplicates. Without an equal section, repeated values could remain in a large recursive problem even though their final order relative to one another does not matter.

## Space Complexity

The deterministic implementation creates lists for the lower, equal, and higher partitions. The total temporary partition storage is O(n) for one selection level. It also creates a list of group medians whose size is approximately n/5. Therefore, the implementation uses O(n) additional space.

The randomized implementation works in place on a copy of the caller's input. Its partition procedure requires only a constant number of indices. The copy itself requires O(n) space. If modifying the original list were allowed, the internal algorithm would require O(1) auxiliary array space.

## Benchmark Design

The benchmark tests four distributions:

- Random values
- Already sorted values
- Reverse-sorted values
- Duplicate-heavy values

The input sizes are 100, 500, 1,000, 2,000, and 5,000. The selected order statistic is the median position. Each result is the median of seven executions.

Before recording a timing, the benchmark compares the returned value with the result obtained from Python's sorted function. This prevents an incorrect result from being treated as a successful performance measurement.

## Benchmark Results

The benchmark compared deterministic Median of Medians with Randomized Quickselect using random, sorted, reverse-sorted, and duplicate-heavy inputs. Each value represents the median execution time across seven runs.

| Size | Distribution | Deterministic Selection (seconds) | Randomized Selection (seconds) |
|---:|---|---:|---:|
| 100 | Random | 0.000014 | 0.000010 |
| 100 | Sorted | 0.000011 | 0.000009 |
| 100 | Reverse | 0.000010 | 0.000007 |
| 100 | Repeated | 0.000005 | 0.000007 |
| 500 | Random | 0.000031 | 0.000043 |
| 500 | Sorted | 0.000049 | 0.000039 |
| 500 | Reverse | 0.000045 | 0.000037 |
| 500 | Repeated | 0.000021 | 0.000031 |
| 1000 | Random | 0.000118 | 0.000096 |
| 1000 | Sorted | 0.000084 | 0.000105 |
| 1000 | Reverse | 0.000091 | 0.000088 |
| 1000 | Repeated | 0.000050 | 0.000069 |
| 2000 | Random | 0.000258 | 0.000180 |
| 2000 | Sorted | 0.000186 | 0.000178 |
| 2000 | Reverse | 0.000179 | 0.000198 |
| 2000 | Repeated | 0.000096 | 0.000114 |
| 5000 | Random | 0.000662 | 0.000687 |
| 5000 | Sorted | 0.000451 | 0.000382 |
| 5000 | Reverse | 0.000456 | 0.000329 |
| 5000 | Repeated | 0.000226 | 0.000273 |

## Discussion of Empirical Results

The benchmark results were generally consistent with the theoretical analysis, although neither algorithm was faster in every test. Randomized Quickselect produced the lower time in several cases, especially for random input at sizes 100, 1,000, and 2,000. For example, at size 2,000 on random data, the randomized implementation completed in 0.000180 seconds, compared with 0.000258 seconds for the deterministic version. This difference is reasonable because Randomized Quickselect selects a pivot directly, while Median of Medians performs additional work to divide the input into small groups, sort those groups, and recursively select a reliable pivot.

The deterministic implementation was faster in some other cases. At size 500 on random input, it completed in 0.000031 seconds compared with 0.000043 seconds for the randomized version. It was also faster on duplicate-heavy input for every tested size. At size 5,000 with repeated values, deterministic selection took 0.000226 seconds, while randomized selection took 0.000273 seconds. Since both algorithms use three-way partitioning, repeated pivot values can be removed from the active problem at once. The deterministic pivot selection also appears to have selected useful pivots consistently for these low-range datasets.

Sorted and reverse-sorted inputs did not create the severe performance problems that are often seen with algorithms that always choose the first or last element as the pivot. Median of Medians does not depend on the original input order, and Randomized Quickselect selects its pivot independently of that order. At size 5,000, the randomized implementation completed sorted input in 0.000382 seconds and reverse-sorted input in 0.000329 seconds. The deterministic version remained stable as well, taking 0.000451 and 0.000456 seconds for the same inputs.

The timing differences were relatively small because the tested input sizes were moderate and both implementations are efficient. Python function-call overhead, list creation, random-number generation, memory allocation, and background system activity can all affect measurements at this scale. For example, the randomized result may vary slightly between benchmark runs because different pivots can lead to different partition sizes.

Overall, the results show the practical trade-off between the two algorithms. Randomized Quickselect often has lower overhead and can be faster in normal use, but its theoretical worst case remains \(O(n^2)\). Median of Medians performs extra work and is not guaranteed to be the fastest in a benchmark, but it provides the stronger guarantee of \(O(n)\) running time even for intentionally difficult input arrangements. The benchmark therefore supports the idea that deterministic selection is valuable when worst-case predictability matters, while randomized selection is often attractive when simpler implementation and strong expected performance are the main priorities.

## Discussion of Empirical Results

On random inputs, Randomized Quickselect will often be faster because it chooses a pivot directly and does not perform the grouping work required by Median of Medians. The deterministic algorithm performs extra operations to obtain its worst-case guarantee, and this overhead is visible even when the randomized pivots happen to be good.

Sorted and reverse-sorted data should not create a systematic problem for either implementation. Median of Medians does not rely on the original ordering, while Randomized Quickselect chooses pivots independently of that order. This differs from deterministic first-pivot Quickselect, which could degrade badly on ordered input.

Duplicate-heavy input should perform well because both implementations group all values equal to the pivot. When the pivot is one of the common repeated values, a large portion of the input can be eliminated in one step.

Small timing differences may not perfectly match the theoretical analysis. Python function-call overhead, list creation, random-number generation, memory allocation, and background system activity can influence short benchmark runs. The main theoretical difference is therefore not that Median of Medians must always be faster, but that it provides a stronger worst-case guarantee.

# Part 2: Elementary Data Structures

## Dynamic Array

The dynamic array stores elements in a fixed-capacity block. When the block becomes full, a larger block is allocated and existing values are copied into it.

Indexed access and updates take O(1) because the address of an element can be determined directly from its index. Inserting or deleting near the beginning takes O(n) because later values must shift.

Appending normally takes O(1). A resize occasionally costs O(n), but capacity is doubled each time. When that occasional cost is distributed across many appends, append remains O(1) amortized.

## Matrix

The matrix is represented as a rectangular collection of rows. Accessing or updating one element takes O(1) because both row and column positions are known.

Inserting or deleting a row may require the outer list to shift row references. Inserting or deleting a column requires visiting every row, so its running time depends on the number of rows.

Matrices are useful when data naturally has two dimensions, including image pixels, game boards, tabular measurements, adjacency matrices, and numerical calculations.

## Stack

The stack follows last-in, first-out order. It uses the end of an array for both insertion and removal, allowing push and pop to run in O(1) amortized time.

Stacks are useful for function-call management, undo operations, expression evaluation, browser navigation, depth-first search, and syntax parsing.

Using the beginning of an array would be less efficient because every push or pop would shift the remaining values.

## Circular Queue

The queue follows first-in, first-out order. A basic array implementation that deletes index zero would require O(n) time because all remaining elements would shift.

The circular queue avoids this problem by maintaining a front index and calculating positions with modular arithmetic. Enqueue and dequeue therefore run in O(1) amortized time.

Queues are useful for request processing, print jobs, message handling, breadth-first search, customer service systems, and event scheduling.

## Singly Linked List

Each linked-list node stores a value and a reference to the next node. Inserting at the front takes O(1) because only the head reference changes.

The implementation also stores a tail reference, allowing insertion at the end in O(1). Without the tail reference, appending would require traversing the list and would take O(n).

Accessing an arbitrary position takes O(n) because linked-list nodes are not stored in contiguous memory. The traversal must begin at the head and follow each reference in sequence.

## Complexity Comparison

| Structure | Operation | Complexity |
|---|---|---:|
| Dynamic Array | Access/update | O(1) |
| Dynamic Array | Append | O(1) amortized |
| Dynamic Array | Insert/delete by position | O(n) |
| Matrix | Access/update | O(1) |
| Matrix | Insert/delete column | O(rows) |
| Stack | Push/pop/peek | O(1) amortized |
| Circular Queue | Enqueue/dequeue/front | O(1) amortized |
| Linked List | Insert at front | O(1) |
| Linked List | Insert at end with tail | O(1) |
| Linked List | Access/search/delete by value | O(n) |

## Arrays Versus Linked Lists

Arrays provide fast indexed access and good cache behavior because values are stored close together. They are a strong choice when applications frequently read elements by position.

Linked lists are useful when insertions at known node locations are more important than random access. They do not require shifting later elements after an insertion. However, every node stores an additional reference, and following nodes may have weaker cache locality.

For stacks, an array is generally simpler and efficient because operations occur at one end. A linked-list stack can also provide O(1) push and pop, but each element requires a node and reference.

For queues, a circular array provides efficient operations and good memory locality. A linked queue can grow one node at a time and does not require resizing, but it has extra pointer overhead and more individual memory allocations.

## Practical Applications

Dynamic arrays are useful for collections that grow over time while still requiring indexed access. Examples include application records, dynamic buffers, and collections returned by service APIs.

Matrices represent two-dimensional relationships and measurements. They appear in graphics, machine learning, scientific computing, maps, and graph representations.

Stacks support operations that must be reversed in the opposite order from which they were created. Examples include undo history, nested function calls, and parsing parentheses.

Queues preserve arrival order. They are common in task scheduling, asynchronous messaging, web request processing, and breadth-first traversal.

Linked lists are useful when the application frequently changes sequence membership and already has references to nearby nodes. They can be used in adjacency lists, memory-management structures, and collision chains in hash tables.

## Design Decisions and Limitations

The implementations prioritize clarity and visible algorithmic behavior rather than replacing Python's production-quality built-in containers.

The deterministic selection implementation uses separate partition lists, which makes duplicate handling and correctness easier to follow. An advanced in-place implementation could reduce array-allocation overhead but would be more complex.

The matrix implementation supports structural changes for learning purposes, although production numerical programs would normally use specialized libraries.

The linked list is singly linked, so traversal is possible only in the forward direction. A doubly linked list would support easier backward movement and deletion when a node reference is known, but every node would require an additional pointer.

# Conclusion

This assignment showed that a strong worst-case guarantee and fast practical performance are not always the same goal. Median of Medians guarantees O(n) selection, but it performs additional pivot-selection work. Randomized Quickselect has a weaker worst-case bound, yet it often performs faster because its pivot selection is inexpensive.

The data structure implementations demonstrated that operation cost depends on how information is stored. Arrays provide direct access, linked lists support inexpensive endpoint insertion, stacks reverse processing order, and queues preserve arrival order.

The main lesson is that algorithm and data structure selection should be based on the operations an application performs most often. Complexity analysis provides a starting point, but memory behavior, implementation overhead, input distribution, and practical requirements also influence the final decision.
