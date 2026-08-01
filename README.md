# Assignment 6: Medians, Order Statistics, and Elementary Data Structures

## Overview

This project contains two selection algorithms and several elementary data structure implementations.

Part 1 compares deterministic selection using Median of Medians with Randomized Quickselect. Both algorithms return the kth smallest value without fully sorting the input.

Part 2 implements a dynamic array, matrix, stack, circular queue, and singly linked list. The goal is to compare their operations, complexity, design trade-offs, and practical uses.

## Repository Structure

```text
deterministic_selection.py
randomized_selection.py
selection_benchmark.py
dynamic_array.py
matrix.py
stack.py
queue.py
linked_list.py
test_assignment.py
report.md
README.md
.gitignore
```

## Requirements

- Python 3.10 or newer
- No third-party libraries are required

## Running the Selection Algorithms

```bash
python3 deterministic_selection.py
python3 randomized_selection.py
```

## Running the Benchmark

```bash
python3 selection_benchmark.py
```

The benchmark tests random, sorted, reverse-sorted, and duplicate-heavy inputs. Each timing is the median of seven runs.

## Running the Data Structure Demonstrations

```bash
python3 dynamic_array.py
python3 matrix.py
python3 stack.py
python3 queue.py
python3 linked_list.py
```

## Running All Tests

```bash
python3 test_assignment.py
```

## Main Findings

Median of Medians provides a worst-case linear-time guarantee because its pivot selection removes a fixed portion of the remaining input during each recursive step. This stronger guarantee comes with additional practical overhead from grouping values, sorting small groups, and recursively selecting the median of their medians.

Randomized Quickselect has expected linear running time and is usually simpler and faster in practice. Its theoretical worst case remains quadratic, but random pivot selection makes repeated poor partitions unlikely.

The data structure implementations also show that no single structure is best for every task. Dynamic arrays provide constant-time indexed access, while linked lists make insertion at the front inexpensive. Stacks are well suited for last-in, first-out processing, and circular queues support efficient first-in, first-out operations without repeatedly shifting elements.

## Complexity Summary

| Component | Operation | Complexity |
|---|---|---:|
| Median of Medians | Selection | O(n) worst case |
| Randomized Quickselect | Selection | O(n) expected |
| Randomized Quickselect | Worst-case selection | O(n²) |
| Dynamic Array | Access/update | O(1) |
| Dynamic Array | Append | O(1) amortized |
| Dynamic Array | Insert/delete | O(n) |
| Matrix | Element access/update | O(1) |
| Stack | Push/pop/peek | O(1) amortized |
| Circular Queue | Enqueue/dequeue/front | O(1) amortized |
| Linked List | Insert at front | O(1) |
| Linked List | Insert at end with tail | O(1) |
| Linked List | Access/search/delete by value | O(n) |
