# Python 3 Object-Oriented Programming 3rd Edition

## Object-Oriented Design

## Objects in Python

## When Objects Are Alike

In the programming world, duplicate code is considered evil.
We should not have multiple copies of the same, or similar, code in different places.

There are many ways to merge pieces of code or objects that have a similar functionality.
In this chapter, we'll be covering the most famous object-oriented principle: inheritance.

### Basic inheritance

Technically, every class we create uses inheritance.
All Python classes are subclasses of the special built-in class named `object`.
This class provides very little in terms of data and behaviors (the behaviors it does provide are all double-underscore methods intended for internal use only), but it does allow Python to treat all objects in the same way.

If we don't explicitly inherit from a different class, our classes will automatically inherit from `object`.

### Multiple inheritance

### Polymorphism

Polymorphism is actually one of the coolest things about object-oriented programming, and it makes some programming designs obvious that weren't possible in earlier paradigms.
However, Python makes polymorphism seem less awesome because of duck typing.
Duck typing in Python allows us to use *any* object that provides the required behavior without forcing it to be a subclass.

### Abstract base classes

While duck typing is useful, it is not always easy to tell in advance if a class is going to fulfill the protocol you require.
Therefore, Python introduced the idea of abstract base classes (ABCs).
Abstract base classes define a set of methods and properties that a class must implement in order to be considered a duck-type instance of that class.
The class can extend the abstract base class itself in order to be used as an instance of that class, but it must supply all the appropriate methods.

#### Using an abstract base class

Most of the abstract base classes that exist in the Python standard library live in the `collections` module.
One of the simplest ones is the `Container` class.

#### Creating an abstract base class

Next, we see the `@abc.abstractmethod` and `@abc.abstractproperty` constructs.
These are Python decorators.
For now, just know that by marking a method or property as being abstract, you are stating that any subclass of this class must implement that method or supply that property in order to be considered a proper member of the class.

More common object-oriented languages have a clear separation between the interface and the implementation of a class.
For example, some languages provide an explicit `interface` keyword that allows us to define the methods that a class must have without any implementation.
In such an environment, an abstract class is one that provides both an interface and a concrete implementation of some, but not all, methods.
Any class can explicitly state that it implements a given interface.

Python's ABCs help to supply the functionality of interfaces without compromising on the benefits of duck typing.

#### Demystifying the magic

```python
@classmethod
```
This decorator marks the method as a class method.
It essentially says that the method can be called on a class instead of an instantiated object.

```python
def __subclasshook__(cls, c):
```
This defines the `__subclasshook__` class method.
This special method is called by the Python interpreter to answer the question: Is the class `C` a subclass of this class?

## Expecting the Unexpected

### Raising exceptions

In principle, an exception is just an object.
There are many different exception classes available, and we can easily define more of our own.
The one thing they all have in common is that they inherit from a built-in class called `BaseException`.
These exception objects become special when they are handled inside the program's flow of control.
When an exception occurs, everything that was supposed to happen doesn't happen, unless it was supposed to happen when an exception occurred.

#### Raising an exception

If either of the two conditions is not met, the `raise` keyword causes an exception to occur.
The `raise` keyword is followed by the object being raised as an exception.

#### The effects of an exception

When an exception is raised, it appears to stop program execution immediately.
Any lines that were supposed to run after the exception is raised are not executed, and unless the exception is dealt with, the program will exit with an error message.

Furthermore, if we have a function that calls another function that raises an exception, nothing is executed in the first function after the point where the second function was called.
Raising an exception stops all execution right up through the function call stack until it is either handled or forces the interpreter to exit.

#### Handling exceptions

We handle exceptions by wrapping any code that might throw one (whether it is exception code itself, or a call to any function or method that may have an exception raised inside it) inside a `try...except` clause.

#### The exception hierarchy

We've already seen several of the most common built-in exceptions, and you'll probably encounter the rest over the course of your regular Python development.
As we noticed earlier, most exceptions are subclasses of the `Exception` class.
But this is not true of all exceptions.
`Exception` itself actually inherits from a class called `BaseException`.
In fact, all exceptions must extend the `BaseException` class or one of its subclasses.

There are two key built-in the exception classes, `SystemExit` and `KeyboardInterrupt`, that derive directly from `BaseException` instead of `Exception`.

When we use the `except:` clause without specifying any type of exception, it will catch all subclasses of `BaseException`; which is to say, it will catch all exceptions, including the two special ones.
Since we almost always want these to get special treatment, it is unwise to use the `except:` statement without arguments.
If you want to catch all exceptions other than `SystemExit` and `KeyboardInterrupt`, explicitly catch `Exception`.
Most Python developers assume that `except:` without a type is an error and will flag it in code review.
If you really do want to catch everything, just explicitly use `except BaseException:`.

#### Defining our own exceptions

Occasionally, when we want to raise an exception, we find that none of the built-in exceptions are suitable.
Luckily, it's trivial to define new exceptions of our own.
The name of the class is usually designed to communicate what went wrong, and we can provide arbitrary arguments in the initializer to include additional information.

All we have to do is inherit from the `Exception` class.
We don't even have to add any content to the class!
We can, of course, extend `BaseException` directly, but I have never encountered a use case where this would make sense.

## When to Use Object-Oriented Programming

### Treat objects as objects

Identifying objects is a very important task in object-oriented analysis and programming.
But it isn't always as easy as counting the nouns in short paragraphs that, frankly, I have constructed explicitly for that purpose.
Remember, objects are things that have both data and behavior.
If we are working only with data, we are often better off storing it in a list, set, dictionary, or other Python data structure.
On the other hand, if we are working only with behavior, but no stored data, a simple function is more suitable.

An object, however, has both data and behavior.
Proficient Python programmers use built-in data structures unless (or until) there is an obvious need to define a class.
There is no reason to add an extra level of abstraction if it doesn't help organize our code.
On the other hand, the *obvious* need is not always self-evident.

We can often start our Python programs by storing data in a few variables.
As the program expands, we will later find that we are passing the same set of related variables to a set of functions.
This is the time to think about grouping both variables and functions into a class.

### Adding behaviors to class data with properties

Python gives us the `property` keyword to make methods that look like attributes.
We can therefore write our code to use direct member access, and if we ever unexpectedly need to alter the implementation to do some calculation when getting or setting that attribute's value, we can do so without changing the interface.

#### Properties in detail

#### Decorators - another way to create properties

#### Deciding when to use properties

Technically, in Python, data, properties, and methods are all attributes on a class.

The fact that methods are just callable attributes, and properties are just customizable attributes, can help us make this decision.
Methods should typically represent actions; things that can be done to, or performed by, the object.
When you call a method, even with only one argument, it should *do* something.
Method names are generally verbs.

Once confirming that an attribute is not an action, we need to decide between standard data attributes and properties.
In general, always use a standard attribute until you need to control access to that property in some way.
In either case, your attribute is usually a noun.
The only difference between an attribute and a property is that we can invoke custom actions automatically when a property is retrieved, set, or deleted.

Let's look at a more realistic example.
A common need for custom behavior is caching a value that is difficult to calculate or expensive to look up (requiring, for example, a network request or database query).
The goal is to store the value locally to avoid repeated calls to the expensive calculation.

Custom getters are also useful for attributes that need to be calculated on the fly, based on other object attributes.

Custom setters are useful for validation, as we've already seen, but they can also be used to proxy a value to another location.

### Manager objects

#### Removing duplicate code

But what should we do instead of code duplication?
The simplest solution is often to move the code into a function that accepts parameters to account for whatever parts are different.
This isn't a terribly object-oriented solution, but it is frequently optimal.

#### In practice

## Python Data Structures

In this chapter, we'll discuss the object-oriented features of these data structures, when they should be used instead of a regular class, and when they should not be used.

### Empty objects

It has been stressed throughout this book that classes and objects should only be used when you want to specify both data and behaviors.
The main reason to write an empty class is to quickly block something out, knowing we'll come back later to add behavior.
It is much easier to adapt behaviors to a class than it is to replace a data structure with an object and change all references to it.
Therefore, it is important to decide from the outset whether the data is just data, or whether it is an object in disguise.
Once that design decision is made, the rest of the design naturally falls into place.

### Tuples and named tuples

Unpacking is a very useful feature in Python.
We can group variables together to make storing and passing them around simpler, but the moment we need to access all of them, we can unpack them into separate variables.

#### Named tuples

If we do not need to add behavior to the object, and we know in advance which attributes we need to store, we can use a named tuple.
Named tuples are tuples with attitude.
They are a great way to group read-only data together.

Constructing a named tuple takes a bit more work than a normal tuple.

### Dataclasses

### Dictionaries

Dictionaries are incredibly useful containers that allow us to map objects directly to other objects.

We can, of course, catch the `KeyError` and handle it.
But we have other options.
Remember, dictionaries are objects, even if their primary purpose is to hold other objects.
As such, they have several behaviors associated with them.
One of the most useful of these methods is the `get` method;
it accepts a key as the first parameter and an optional default value if the key doesn't exist:
```python
>>> print(stocks.get("RIM"))
None
>>> stocks.get("RIM", "NOT FOUND")
'NOT FOUND'
```

Three other very useful dictionary methods are `keys()`, `values()`, and `items()`.
The first two return an iterator over all the keys and all the values in the dictionary.
We can use these like lists or in for loops if we want to process all the keys or values.
The `items()` method is probably the most useful;
it returns an iterator over tuples of `(key, value)` pairs for every item in the dictionary.
This works great with tuple unpacking in a `for` loop to loop over associated keys and values.

Objects that are **hashable** basically have a defined algorithm that converts the object into a unique integer value for rapid lookup in the dictionary.
This hash is what is actually used to find values in a dictionary.

#### Dictionary use cases

#### Using `defaultdict`

### Lists

Lists are the least object-oriented of Python's data structures.
While lists are, themselves, objects, there is a lot of syntax in Python to make using them as painless as possible.
Unlike many other object-oriented languages, lists in Python are simply available.
We don't need to import them and rarely need to call methods on them.
We can loop over a list without explicitly requesting an iterator object, and we can construct a list (as with a dictionary) with custom syntax.
Further, list comprehensions and generator expressions turn them into a veritable Swiss Army knife of computing functionality.

#### Sorting lists

Without any parameters, `sort` will generally do as expected.

If we want to place objects we define ourselves into a list and make those objects sortable, we have to do a bit more work.
The special `__lt__`  method, which stands for less than, should be defined on the class to make instances of that class comparable.
The `sort` method on the list will access this method on each object to determine where it goes in the list.
This method should return `True` if our class is somehow less than the passed parameter, and `False` otherwise.
