# Mastering Object-Oriented Python 2nd Edition

## Preliminaries, Tools, and Techniques

We've chosen a problem domain that's relatively simple: the strategies for playing the game of *blackjack*.

### Technical requirements

### About the Blackjack game

### The Python runtime and special methods

One of the essential concepts for mastering object-oriented Python is to understand how object methods are implemented.

This is a core pattern of Python: the simple operator-like syntax is implemented by special methods.
The special methods have names surrounded with `__` to make them distinctive.

### Interaction, scripting, and tools

Python is often described as *Batteries Included* programming.
Everything required is available directly as part of a single download.
This provides the runtime, the standard library, and the IDLE editor as a simple development environment.

### Selecting an IDE

### Consistency and style

### Type hints and the mypy program

Python 3 permits the use of type hints.
The hints are present in assignment statements, function, and class definitions.
They're not used directly by Python when the program runs.
Instead, they're used by external tools to examine the code for improper use of types, variables, and functions.

### Performance - the `timeit` module

### Testing - `unittest` and `doctest`

### Documentation - sphinx and RST markup

### Installing components

## The `__init__()` Method

### Composite objects

A composite object can also be called a **container**.

Before designing a new class, we need to ask this question: is using a simple `list` object appropriate?

Some programmers rush to define new classes as if using a built-in class violates some object-oriented design principle.

Defining a class has the advantage of creating a simplified, implementation-free interface to the object.

To design a collection of objects, we have the following three general design strategies:
* **Wrap**: This design pattern surrounds an existing collection definition with a simplified interface.
This is an example of the more general **Facade** design pattern.
* **Extend**: This design pattern starts with an existing collection class and extends it to add features.
* **Invent**: This is designed from scratch.

These three concepts are central to object-oriented design.
Because Python has so many features built into the language, we must always make this choice when designing a class.

#### Wrapping a collection class

The following is a wrapper design that contains an internal collection:
```python
class Deck:
    def __init__(self) -> None:
        self._cards = [card(r + 1, s) for r in range(13) for s in iter(Suit)]
        random.shuffle(self._cards)

    def pop(self) -> Card:
        return self._cards.pop()
```

Generally, a **Facade** design pattern or **wrapper** class contains methods that delegate the work to the underlying implementation class.
This delegation can become wordy when a lot of features are provided.
For a sophisticated collection, we may wind up delegating a large number of methods to the wrapped object.
