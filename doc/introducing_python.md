# Introducing Python

## Data: Types, Values, Variables, and Names

### Python Data Are Objects

### Types

### Variables

Within a Python program, you can find the reserved words with
```python
help("keywords")
```
or:
```python
import keyword
keyword.kwlist
```

### Assignment

In Python, you use `=` to *assign* a value to a variable.

### Variables Are Names, Not Places

Now it's time to make a crucial point about variables in Python: *variables are just names*.
This is different from many other computer languages, and a key thing to know about Python, especially when we get to *mutable* objects like lists.
Assignment *does not copy* a value;
it just *attaches a name* to the object that contains the data.
The name is a *reference* to a thing rather than the thing itself.

### Reassigning a Name

### Copying

## Numbers

### Booleans

In Python, the only values for the boolean data type are `True` and `False`.
Sometimes, you'll use these directly;
other times you'll evaluate the "truthiness" of other types from their values.
The special Python function `bool()` can convert any Python datatype to a boolean.

### Integers

## Choose with `if`

### Comment with `#`

A comment is a piece of text in your program that is ignored by the Python interpreter.
You might use comments to clarify nearby Python code,make notes to yourself to fix something someday,or for whatever purpose you like.
You mark a comment by using the `#` character;
everything from that point on to the end of the current line is part of the comment.

### New: I Am the Walrus

## Text Strings

Unlike other languages, strings in Python are *immutable* .
You can't change a string in place, but you can copy parts of strings to another string to get the same effect.

### Create with Quotes

### Get a Substring with a Slice

### Get Length with `len()`

### Split with `split()`

### Case

### Formatting

#### Newest Style: f-strings

*f-strings* appeared in Python 3.6, and are now the recommended way of formatting strings.

## Loop with `while` and `for`

## Tuples and Lists

### Lists

#### Copy Everything with `deepcopy()`

## Dictionaries and Sets

## Functions

### Define a Function with `def`

To define a Python function, you type `def`, the function name, parentheses enclosing any input parameters to the function, and then finally, a colon (`:`).

### Call a Function with Parentheses

### Arguments and Parameters

### Docstrings

### Inner Functions

### Anonymous Functions: lambda

A Python *lambda function* is an anonymous function expressed as a single statement.
You can use it instead of a normal tiny function.

A lambda has zero or more comma-separated arguments, followed by a colon (`:`), and then the definition of the function.

### Use of `_` and `__` in Names

## Objects and Classes

### Methods

### Initialization

### Get Help from Your Parent with `super()`

### Method Types

### Dataclasses

## Modules, Packages, and Goodies

### Modules and the `import` statement

#### Import a Module

### Packages

### Goodies in the Python Standard Library

#### Handle Missing Keys with `setdefault()` and `defaultdict()`

`defaultdict()` is similar, but specifies the default value for any new key up front, when the dictionary is created.
Its argument is a function.

#### Order by Key with `OrderedDict()`
