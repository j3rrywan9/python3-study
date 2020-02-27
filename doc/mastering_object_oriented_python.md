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

### The implicit superclass - `object`

Each Python class definition has an implicit superclass: `object`.
It's a very simple class definition that does almost nothing.

When we define our own class, `object` is the superclass.

We can see that a class is an object of the class named `type` and that the base class for our new class is the class named `object`.
As we look at each method, we also take a look at the default behavior inherited from `object`.
In some cases, the superclass special method's behavior will be exactly what we want.
In other cases, we'll need to override the behavior of the special method.

### The base class object `__init__()` method

The superclass of all classes, `object`, has a default implementation of `__init__()` that amounts to `pass`.
We aren't required to implement `__init__()`.
If we don't implement it, then no instance variables will be created when the object is created.
In some cases, this default behavior is acceptable.

### Implementing `__init__()` in a superclass

We initialize an object by implementing the `__init__()` method.
When an object is created, Python first creates an empty object and then calls the `__init__()` method to set the state of the new object.
This method generally creates the object's instance variables and performs any other one-time processing.

The leading `_` in the name is a suggestion to someone reading the class that the `_points()` method is an implementation detail, subject to change in a future implementation.
This can help to reveal which methods are part of a public interface and which are details that aren't intended for general use by other classes.

### Leveraging `__init__()` via a factory function

In Python, there are two common approaches to factories, as follows:
* We define a function that creates  objects of the required classes.
* We define a class that has methods for creating objects.
This is the **Factory** design pattern, as described in books on object-oriented design patterns.

In Python, a class isn't required to create an object factory, but this can be a good idea when there are related factories or factories that are complex.
One of the strengths of Python is that we're not forced to use a class hierarchy when a simple function might do just as well.

The advantage of class definitions is code reuse via inheritance.
The purpose of a factory class is to encapsulate the complexities of object construction in a way that's extensible.
If we have a factory class, we can add subclasses when extending the target class hierarchy.
This can give us polymorphic factory classes; different factory class definitions can have the same method signatures and can be used interchangeably.

If the alternative factory definitions don't actually reuse any code, then a class hierarchy won't be as helpful in Python.
We can simply use functions that have the same signatures.

#### Faulty factory design and the vague else clause

#### Simplicity and consistency using `elif` sequences

#### Simplicity and consistency using mapping and class objects

### Implementing `__init__()` in each subclass

This often requires some common initialization of a superclass as well as subclass-specific initialization.
We need to follow the **Don't Repeat Yourself (DRY)** principle to keep the code from getting cloned into each of the subclasses.

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
