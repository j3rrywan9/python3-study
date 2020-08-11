# Introducing Python, 2nd Edition

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

To make an f-string:
* Type the letter f or F directly before the initial quote.
* Include variable names or expressions within curly brackets (`{}`) to get their values into the string.

It's like the previous section's "new-style" formatting,but without the `format()` function, and without empty brackets (`{}`) or positional ones (`{1}`)in the format string.

As I already mentioned, expressions are also allowed inside the curly brackets:
```python
f'The {thing.capitalize()} is in the {place.rjust(20)}'
```
This means that the things that you could do inside `format()` in the previous section, you can now do inside a `{}` in your main string.
This seems easier to read.

## Loop with `while` and `for`

## Tuples and Lists

### Lists

#### Copy Everything with `deepcopy()`

## Dictionaries and Sets

### Dictionaries

A *dictionary* is similar to a list, but the order of items doesn't matter, and they aren't selected by an offset such as 0 or 1.
Instead,you specify a unique key to associate with each value.
This key is often a string, but it can actually be any of Python's immutable types: boolean, integer, float, tuple, string, and others that you'll see in later chapters.
Dictionaries are mutable, so you can add, delete, and change their key-value elements.

#### Convert with `dict()`

#### Add or Change an Item by `[key]`

#### Get an Item by `[key]` or with `get()`

The second is to use the special dictionary `get()` function.
You provide the dictionary, key, and an optional value.

#### Get All Keys with `keys()`

You can use `keys()` to get all of the keys in a dictionary.

In Python 3, you also need to use the `list()` function to turn the results of `values()` and `items()` into normal Python lists.

#### Get All Values with `values()`

#### Get All Key-Value Pairs with `items()`

#### Delete an Item by Key with `del()`

#### Delete All Items with `clear()`

#### Test for a Key with `in`

#### Copy Everything with `deepcopy()`

#### Iterate with `for` and `in`

Iterating over a dictionary (or its `keys()` function) returns the keys.

#### Dictionary Comprehensions

### Sets

#### Create with `set()`

#### Add an Item with `add()`

#### Delete an Item with `remove()`

#### Iterate with `for` and `in`

#### Test for a Value with `in`

#### Combinations and Operators

## Functions

### Define a Function with `def`

To define a Python function, you type `def`, the function name, parentheses enclosing any input parameters to the function, and then finally, a colon (`:`).

Even for a function with no parameters like this one,you still need the parentheses and the colon in its definition.
The next line needs to be indented, just as you would indent code under an `if` statement.
Python requires the `pass` statement to show that this function does nothing.

### Call a Function with Parentheses

### Arguments and Parameters

The values you pass into the function when you call it are known as *arguments*.
When you call a function with arguments, the values of those arguments are copied to their corresponding *parameters* inside the function.

### `None` Is Useful

`None` is a special Python value that holds a place when there is nothing to say.
It is not the same as the boolean value `False`, although it looks false when evaluated as a boolean.

To distinguish `None` from a boolean `False` value, use Python's `is` operator:

This seems like a subtle distinction, but it's important in Python.
You'll need `None` to distinguish a missing value from an empty value.

### Positional Arguments

Python handles function arguments in a manner that's very flexible, when compared to many languages.
The most familiar types of arguments are *positional arguments*, whose values are copied to their corresponding parameters in order.

Although very common, a downside of positional arguments is that you need to remember the meaning of each position.

### Keyword Arguments

To avoid positional argument confusion, you can specify arguments by the names of their corresponding parameters, even in a different order from their definition in the function:

You can mix positional and keyword arguments.

If you call a function with both positional and keyword arguments, the positional arguments need to come first.

### Specify Default Parameter Values

You can specify default values for parameters.
The default is used if the caller does not provide a corresponding argument.

### Explode/Gather Positional Arguments with `*`

When used inside the function with a parameter, an asterisk groups a variable number of positional arguments into a single tuple of parameter values.

This is useful for writing functions such as `print()` that accept a variable number of arguments.
If your function has required positional arguments, as well, put them first;
`*args` goes at the end and grabs all the rest:
```python
def print_more(required1, required2, *args):
    print('Need this one:', required1)
    print('Need this one too:', required2)
    print('All the rest:', args)
```

### Explode/Gather Keyword Arguments with `**`

You can use two asterisks (`**`) to group keyword arguments into a dictionary, where the argument names are the keys, and their values are the corresponding dictionary values.

Inside the function, `kwargs` is a dictionary parameter.

### Keyword-Only Arguments

### Mutable and Immutable Arguments

### Docstrings

You can attach documentation to a function definition by including a string at the beginning of the function body.
This is the function's *docstring*:

### Functions Are First-Class Citizens

Functions are first-class citizens in Python.
You can assign them to variables, use them as arguments to other functions, and return them from functions.

In Python, those parentheses mean call this function.
With no parentheses, Python just treats the function like any other object.
That's because, like everything else in Python, it is an object:

You can use functions as elements of lists, tuples, sets, and dictionaries.
Functions are immutable, so you can also use them as dictionary keys.

### Inner Functions

You can define a function within another function:

An inner function can be useful when performing some complex task more than once within another function, to avoid loops or code duplication.

### Anonymous Functions: lambda

A Python *lambda function* is an anonymous function expressed as a single statement.
You can use it instead of a normal tiny function.

A lambda has zero or more comma-separated arguments, followed by a colon (`:`), and then the definition of the function.

### Generators

#### Generator Functions

#### Generator Comprehensions

### Decorators

### Namespaces and Scope

### Use of `_` and `__` in Names

### Recursion

### Async Functions

### Exceptions

When things go south, Python uses exceptions: code that is executed when an associated error occurs.

When you run code that might fail under some circumstances, you also need appropriate exception handlers to intercept any potential errors.

It's good practice to add exception handling anywhere an exception might occur to let the user know what is happening.
You might not be able to fix the problem, but at least you can note the circumstances and shut your program down gracefully.
If an exception occurs in some function and is not caught there, it bubbles up until it is caught by a matching handler in some calling function.
If you don't provide your own exception handler, Python prints an error message and some information about where the error occurred and then terminates the program, as demonstrated in the following snippet:

#### Handle Errors with `try` and `except`

#### Make Your Own Exceptions

You can also define your own exception types to handle special situations that might arise in your own programs.

An exception is a class.
It is a child of the class `Exception`.

## Objects and Classes

### Simple Objects

#### Define a Class with `class`

To create a new object that no one has ever created before, you first define a *class* that indicates what it contains.

To create your own custom object in Python, you first need to define a class by using the `class` keyword.

You create an object from a class by calling the class name as though it were a function:
```python
a_cat = Cat()
another_cat = Cat()
```

#### Attributes

An *attribute* is a variable inside a class or object.
During and after an object or class is created, you can assign attributes to it.
An attribute can be any other object.

#### Methods

A *method* is a function in a class or object.

#### Initialization

If you want to assign object attributes at creation time, you need the special Python object initialization method `__init__()`:

### Inheritance

One solution is inheritance:creating a new class from an existing class, but with some additions or changes.
It's a good way to reuse code.
When you use inheritance, the new class can automatically use all the code from the old class but without you needing to copy any of it.

#### Inherit from a Parent Class

You define only what you need to add or change in the new class, and this overrides the behavior of the old class.
The original class is called a *parent*, *superclass*, or *base class*;
the new class is called a *child*, *subclass*, or *derived class*.

You can check whether a class is derived from another class by using `issubclass()`:
```python
issubclass(Yugo, Car)
```

#### Override a Method

As you just saw, a new class initially inherits everything from its parent class.
Moving forward, you'll see how to replace or override a parent method.

#### Add a Method

The child class can also *add* a method that was not present in its parent class.

#### Get Help from Your Parent with `super()`

Use `super()` when the child is doing something its own way but still needs something from the parent (as in real life).

#### Multiple Inheritance

#### Mixins

You may include an extra parent class in your class definition, but as a helper only.
That is, it doesn't share any methods with the other parent classes, and avoids the method resolution ambiguity that I mentioned in the previous section.

Such a parent class is sometimes called a *mixin* class.
Uses might include "side" tasks like logging.

### In `self` Defense

### Attribute Access

In Python, object attributes and methods are normally public, and you're expected to behave yourself (this is sometimes called a "consenting adults" policy).

#### Direct Access

#### Getters ans Setters

#### Properties for Attribute Access

#### Properties for Computed Values

#### Name Mangling for Privacy

Python has a naming convention for attributes that should not be visible outside of their class definition: begin with two underscores (`__`).

#### Class and Object Attributes

### Method Types

#### Instance Methods

When you see an initial `self` argument in methods within a class definition, it's an *instance method*.
These are the types of methods that you would normally write when creating your own classes.
The first parameter of an instance method is `self`, and Python passes the object to the method when you call it.

#### Class Methods

In contrast, a *class method* affects the class as a whole.
Any change you make to the class affects all of its objects.
Within a class definition,a preceding `@classmethod` decorator indicates that that following function is a class method.
Also, the first parameter to the method is the class itself.
The Python tradition is to call the parameter `cls`, because `class` is a reserved word and can't be used here.

#### Static Methods

A third type of method in a class definition affects neither the class nor its objects;
it's just in there for convenience instead of floating around on its own.
It's a *static method*, preceded by a `@staticmethod` decorator, with no initial `self` or `cls` parameter.

### Duck Typing

### Magic Methods

### Aggregation and Composition

### Dataclasses

Many people like to create objects mainly to store data (as object attributes), not so much behavior (methods).
You just saw how named tuples can be an alternative data store.
Python 3.7 introduced *dataclasses*.

## Modules, Packages, and Goodies

### Modules and the `import` statement

A *module* is just a file of any Python code.
You don’t need to do anything special - any Python code can be used as a module by others.

#### Import a Module

The simplest use of the `import` statement is import *module*, where *module* is the name of another Python file, without the *.py* extension.

#### Import a Module with Another Name

#### Import Only What You Want from a Module

### Packages

To allow Python applications to scale even more, you can organize modules into file and module hierarchies called *packages*.
A package is just a subdirectory that contains *.py* files.
And you can go more than one level deep, with directories inside those.

#### The Module Search Path

To see all the places that your Python interpreter looks, import the standard `sys` module and use its `path` list.
This is a list of directory names and ZIP archive files that Python searches in order to find modules to import.

That initial blank output line is the empty string '', which stands for the current directory.
If '' is first in `sys.path`, Python looks in the current directory first when you try to import something:

The first match will be used.
This means that if you define a module named `random`and it's in the search path before the standard library, you won't be able to access the standard library's `random` now.

#### Relative and Absolute Imports

### Goodies in the Python Standard Library

#### Handle Missing Keys with `setdefault()` and `defaultdict()`

`defaultdict()` is similar, but specifies the default value for any new key up front, when the dictionary is created.
Its argument is a function.

#### Count Items with `Counter()`

#### Order by Key with `OrderedDict()`

#### Stack + Queue == deque

A `deque` (pronounced *deck*) is a double-ended queue, which has features of both a stack and a queue.
It's useful when you want to add and delete items from either end of a sequence.

The function `popleft()` removes the left most item from the deque and returns it;
`pop()` removes the rightmost item and returns it.

## Wrangle and Mangle Data

### Text Strings: Unicode

### Text Strings: Regular Expression

It's time to explore more complex pattern matching by using *regular expressions*.
These are provided in the standard module `re`, which we'll import.
You define a string *pattern* that you want to match, and the *source* string to match against.

#### Find Exact Beginning Match with `match()`

#### Find First Match with `search()`

#### Find All Matches with `findall()`

## Calendars and Clocks

## Files and Directories

### File Input and Output

#### Create or Open with `open()`

You need to call the `open` function before you do the following:
* Read an existing file
* Write to a new file
* Append to an existing file
* Overwrite an existing file

```python
fileobj = open(filename, mode)
```

#### Write a Text File with `print()`

#### Write a Text File with `write()`

#### Read a Text File with `read()`, `readline()`, or `readlines()`

You can provide a maximum character count to limit how much `read()` returns at one time.

You can also read the file a line at a time by using `readline()`.

The easiest way to read a text file is by using an iterator.
This returns one line at a time.

#### Write a Binary File with `write()`

#### Read a Binary File with `read()`

This one is simple;
all you need to do is just open with 'rb':

#### Close Files Automatically by Using `with`

If you forget to close a file that you've opened, it will be closed by Python after it's no longer referenced.
This means that if you open a file within a function and don't close it explicitly, it will be closed automatically when the function ends.
But you might have opened the file in a long-running function or the main section of the program.
The file should be closed to force any remaining writes to be completed.

#### Change Position with `seek()`

### Memory Mapping

### File Operations

#### Check Existence with `exists()`

#### Check Type with `isfile()`

### Directory Operations

### Pathnames

### `BytesIO` and `StringIO`

## Data in Time: Processes and Concurrency

### Programs and Processes

#### Create a Process with `subprocess`

### Command Automation

### Concurrency
