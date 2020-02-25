# Effective Python

## Pythonic Thinking

It's important for you to know the best - the *Pythonic* - way to do the most common things in Python.
These patterns will affect every program you write.

### Item 1: Know which version of Python you're using

Many computers come with multiple versions of the standard CPython runtime preinstalled.
To find out exactly which version of Python you're using, you can use the `--version` flag:
```bash
$ python --version
```

You can also figure out the version of Python you're using at runtime by inspecting values in the `sys` built-in module:
```python
import sys
print(sys.version_info)
print(sys.version)
```

### Item 2: Follow the PEP 8 style guide

Python Enhancement Proposal #8, otherwise known as PEP 8, is the style guide for how to format Python code.
You are welcome to write Python code any way you want, as long as it has valid syntax.
However, using a consistent style makes your code more approachable and easier to read.
Sharing a common style with other Python programmers in the larger community facilitates collaboration on projects.

#### Whitespace

#### Naming

PEP 8 suggests unique styles of naming for different parts in the language.
These conventions make it easy to distinguish which type corresponds to each name when reading code.
Follow these guidelines related to naming:
* Functions, variables, and attributes should be in `lowercase_underscore` format.
* Instance methods in classes should use `self`, which refers to the object, as the name of the first parameter.
* Class methods should use `cls`, which refers to the class, as the name of the first parameter.

#### Expressions and Statements

#### Imports

### Item 3

### Item 4: Prefer interpolated f-strings over C-style format strings and `str.format`

#### Interpolated Format Strings

### Item 5: Write helper functions instead of complex expressions

As soon as expressions get complicated, it's time to consider splitting them into smaller pieces and moving logic into helper functions.
What you gain in readability always outweighs what brevity may have afforded you.
Avoid letting Python's pithy syntax for complex expressions from getting you into a mess like this.
Follow the *DRY principle*: Don't repeat yourself.

### Item 6: Prefer multiple assignment unpacking over indexing

### Item 7: Prefer `enumerate` over `range`

### Item 8: Use `zip` to process iterators in parallel

### Item 9: Avoid `else` blocks after `for` and `while` loops

### Item 10: Prevent repetition with assignment expressions

An assignment expression — also known as the *walrus operator* - is a new syntax introduced in Python 3.8 to solve a long-standing problem with the language that can cause code duplication.
Whereas normal assignment statements are written `a = b `and pronounced "a equals b", these assignments are written `a := b` and pronounced "a walrus b" (because `:=` looks like a pair of eyeballs and tusks).

Assignment expressions are useful because they enable you to assign variables in places where assignment statements are disallowed, such as in the conditional expression of an `if` statement.
An assignment expression's value evaluates to whatever was assigned to the identifier on the left side of the walrus operator.

## Lists and Dictionaries

### Item 11: Know how to slice sequences

Python includes syntax for *slicing* sequences into pieces.
Slicing allows you to access a subset of a sequence's items with minimal effort.
The simplest uses for slicing are the built-in types `list`, `str`, and `bytes`.
Slicing can be extended to any Python class that implements the __getitem__ and __setitem__ special methods

### Item 12

### Item 13

### Item 14: Sort by complex criteria using the `key` parameter

### Item 15

### Item 16: Prefer `get` over `in` and `KeyError` to handle missing dictionary keys

The three fundamental operations for interacting with dictionaries are accessing, assigning, and deleting keys and their associated values.
The contents of dictionaries are dynamic, and thus it's entirely possible - even likely - that when you try to access or delete a key, it won't already be present.

This flow of fetching a key that exists or returning a default value is so common that the `dict` built-in type provides the `get` method to accomplish this task.
The second parameter to `get` is the default value to return in the case that the key - the first parameter - isn't present.

### Item 17

### Item 18

## Functions

### Item 19

To avoid these problems, you should never use more than three variables when unpacking the multiple return values from a function.

### Item 20: Prefer raising exceptions to returning `None`

The second, better way to reduce these errors is to never return `None` for special cases.
Instead, raise an `Exception` up to the caller and have the caller deal with it.

### Item 21: Know how closures interact with variable scope

### Item 22: Reduce visual noise with variable positional arguments

Accepting a variable number of positional arguments can make a function call clearer and reduce visual noise.
(These positional arguments are often called varargs for short, or star args, in reference to the conventional name for the parameter *args.)

### Item 23: Provide optional behavior with keyword arguments

As in most other programming languages, in Python you may pass arguments by position when calling a function:
```python
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6
```
All normal arguments to Python functions can also be passed by keyword, where the name of the argument is used in an assignment within the parentheses of a function call.
The keyword arguments can be passed in any order as long as all of the required positional arguments are specified.
You can mix and match keyword and positional arguments.

Positional arguments must be specified before keyword arguments:

And if you'd like for a function to receive any named keyword argument, you can use the `**kwargs` catch-all parameter to collect those arguments into a dict that you can then process

### Item 24: Use `None` and docstings to specify dynamic default arguments

A default argument value is evaluated only once per module load, which usually happens when a program starts up.

The convention for achieving the desired result in Python is to provide a default value of `None` and to document the actual behavior in the docstring.

When your code sees the argument value `None`, you allocate the default value accordingly:

### Item 25: Enforce clarity with keyword-only and positional-only arguments

### Item 26: Define function decorators with `functools.wraps`

Python has special syntax for decorators that can be applied to functions.
A decorator has the ability to run additional code before and after each call to a function it wraps.
This means decorators can access and modify input arguments, return values, and raised exceptions.
This functionality can be useful for enforcing semantics, debugging, registering functions, and more.

The solution is to use the `wraps` helper function from the `functools` built-in module.
This is a decorator that helps you write decorators.
When you apply it to the `wrapper` function, it copies all of the important metadata about the inner function to the outer function:

## Comprehensions and Generators

### Item 27: Use comprehensions instead of `map` and `filter`

Python provides compact syntax for deriving a new `list` from another sequence or iterable.
These expressions are called *list comprehensions*.

## Classes and Interfaces

### Item 37

### Item 38: Accept functions instead of classes for simple interfaces

Many of Python's built-in APIs allow you to customize behavior by passing in a function.
These hooks are used by APIs to call back your code while they execute.
For example, the `list` type's `sort` method takes an optional `key` argument that's used to determine each index's value for sorting.

### Item 39: Use `@classmethod` polymorphism to construct objects generically

Polymorphism enables multiple classes in a hierarchy to implement their own unique versions of a method.
This means that many classes can fulfill the same interface or abstract base class while providing different functionality.
