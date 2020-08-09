# Data Types

## 2.7

## 3.8

### collections - Container datatypes

This module implements specialized container datatypes providing alternatives to Python's general purpose built-in containers, `dict`, `list`, `set`, and `tuple`.

#### `Counter` objects

A counter tool is provided to support convenient and rapid tallies.

#### deque

#### defaultdict

####  namedtuple

#### OrderedDict

### heapq - Heap queue algorithm

This module provides an implementation of the heap queue algorithm, also known as the priority queue algorithm.

To create a heap, use a list initialized to `[]`, or you can transform a populated list into a heap via function `heapify()`.

The following functions are provided:
```python
heapq.heappush(heap, item)
```
Push the value *item* onto the *heap*, maintaining the heap invariant.
```python
heapq.heappop(heap)
```
Pop and return the smallest item from the *heap*, maintaining the heap invariant.
If the heap is empty, `IndexError` is raised.
To access the smallest item without popping it, use `heap[0]`.
```python
heapq.heapify(x)
```
Transform list *x* into a heap, in-place, in linear time.
```python
heapq.nlargest(n, iterable, key=None)
```
Return a list with the *n* largest elements from the dataset defined by *iterable*.
*key*, if provided, specifies a function of one argument that is used to extract a comparison key from each element in *iterable* (for example, `key=str.lower`).
Equivalent to: `sorted(iterable, key=key, reverse=True)[:n]`.
```python
heapq.nsmallest(n, iterable, key=None)
```
Return a list with the *n* smallest elements from the dataset defined by iterable.
*key*, if provided, specifies a function of one argument that is used to extract a comparison key from each element in *iterable* (for example, `key=str.lower`).
Equivalent to: `sorted(iterable, key=key)[:n]`.

### pprint - Data pretty printer

### enum - Support for enumerations
