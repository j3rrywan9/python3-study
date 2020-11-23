# Python 3 Object-Oriented Programming 3rd Edition

## Object-Oriented Design

In software development, design is often considered as the step done *before* programming.
This isn't true;
in reality, analysis, programming, and design tend to overlap, combine, and interweave.

### Introducing object-oriented

Formally, an object is a collection of **data** and associated **behaviors**.

### Objects and classes

Classes describe objects.
They are like blueprints for creating an object.

### Specifying attributes and behaviors

### Hiding details and creating the public interface

### Composition

Composition is the act of collecting several objects together to create a new one.

### Inheritance

#### Inheritance provides abstraction

#### Multiple inheritance

## Objects in Python

### Creating Python classes

#### Adding attributes

In fact, we don't have to do anything special in the class definition.
We can set arbitrary attributes on an instantiated object using dot notation:
```python
class Point:
    pass

p1 = Point()
p2 = Point()

p1.x = 5
p1.y = 4

p2.x = 3
p2.y = 6

print(p1.x, p1.y)
print(p2.x, p2.y)
```

#### Making it do something

##### Talking to yourself

The one difference, syntactically, between methods and normal functions is that all methods have one required argument.
This argument is conventionally named `self`;
I've never seen a Python programmer use any other name for this variable (convention is a very powerful thing).

The `self` argument to a method is a reference to the object that the method is being invoked on.
We can access attributes and methods of that object as if it were any another object.

##### More arguments

#### Initializing the object

Most object-oriented programming languages have the concept of a **constructor**, a special method that creates and initializes the object when it is created.
Python is a little different; it has a constructor *and* an initializer.

The Python initialization method is the same as any other method, except it has a special name, `__init__`.
The leading and trailing double underscores mean this is a special method that the Python interpreter will treat as a special case.

#### Explain yourself

### Modules and packages

For small programs, we can just put all our classes into one file and add a little script at the end of the file to start them interacting.
However, as our projects grow, it can become difficult to find the one class that needs to be edited among the many classes we've defined.
This is where **modules** come in.
Modules are simply Python files, nothing more.
The single file in our small program is a module.
Two Python files are two modules.
If we have two files in the same folder, we can load a class from one module for use in the other module.

#### Organizing modules

A **package** is a collection of modules in a folder.
The name of the package is the name of the folder.
We need to tell Python that a folder is a package to distinguish it from other folders in the directory.
To do this, place a (normally empty) file in the folder named `__init__.py`.
If we forget this file, we won't be able to import modules from that folder.

### Organizing module content

Every module has a `__name__` special variable that specifies the name of the module when it was imported.
When the module is executed directly with `python module.py`, it is never imported, so the `__name__` is arbitrarily set to the `"__main__"` string.
Make it a policy to wrap all your scripts in an `if __name__ == "__main__":` test, just in case you write a function that you may want to be imported by other code at some point in the future.

### Who can access my data?

By convention, we should also prefix an internal attribute or method with an underscore character, `_`.
Python programmers will interpret this as this is an internal variable, think three times before accessing it directly.
But there is nothing inside the interpreter to stop them from accessing it if they think it is in their best interest to do so.

There's another thing you can do to strongly suggest that outside objects don't access a property or method: prefix it with a double underscore, `__`.
This will perform **name mangling** on the attribute in question.
In essence, name mangling means that the method can still be called by outside objects if they really want to do so, but it requires extra work and is a strong indicator that you demand that your attribute remains **private**.

### Third-party libraries

Instead, Python 3.4 (and higher) supplies the `venv` tool.
This utility basically gives you a mini Python installation called a *virtual environment* in your working directory.
When you activate the mini Python, commands related to Python will work on that directory instead of the system directory.
So, when you run `pip` or `python`, it won't touch the system Python at all.

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

### Sets

In Python, sets can hold any hashable object, not just numbers.
Hashable objects are the same objects that can be used as keys in dictionaries; so again, lists and dictionaries are out.
Like mathematical sets, they can store only one copy of each object.

There is no built-in syntax for an empty set as there is for lists and dictionaries; we create a set using the `set()` constructor.
However, we can use the curly braces (borrowed from dictionary syntax) to create a set, so long as the set contains values.

Sets are inherently unordered due to a hash-based data structure for efficiency.
Because of this lack of ordering, sets cannot have items looked up by index.
The primary purpose of a set is to divide the world into two groups: things that are in the set, and things that are not in the set.
It is easy to check whether an item is in a set or to loop over the items in a set, but if we want to sort or order them, we have to convert the set to a list.

### Extending built-in functions

When we have a built-in container object that we want to add functionality to, we have two options.
We can either create a new object, which holds that container as an attribute (composition), or we can subclass the built-in object and add or adapt methods on it to do what we want (inheritance).

Composition is usually the best alternative if all we want to do is use the container to store some objects using that container's features.
That way, it's easy to pass that data structure into other methods and they will know how to interact with it.
But we need to use inheritance if we want to change the way the container actually works.

Yes, lists are objects.
All that special non-object-oriented looking syntax we've been looking at for accessing lists or dictionary keys, looping over containers, and similar tasks, is actually *syntactic sugar* that maps to an object-oriented paradigm underneath.

Python programmers agree that the non-object-oriented syntax is easier both to read and to write.
Yet all of the preceding Python syntaxes map to object-oriented methods underneath the hood.
These methods have special names (with double-underscores before and after) to remind us that there is a better syntax out there.
However, it gives us the means to override these behaviors.

So, to get back to the earlier point about when we would want to use composition versus inheritance: if we need to somehow change any of the methods on the class, including the special methods, we definitely need to use inheritance.
If we used composition, we could write methods that perform the validation or alterations and ask the caller to use those methods, but there is nothing stopping them from accessing the property directly.

Often, the need to extend a built-in data type is an indication that we're using the wrong sort of data type.
It is not always the case, but if we are looking to extend a built-in, we should carefully consider whether or not a different data structure would be more suitable.

## Python Object-Oriented Shortcuts

### Python built-in functions

There are numerous functions in Python that perform a task or calculate a result on certain types of objects without being methods on the underlying class.
They usually abstract common calculations that apply to multiple types of classes.
This is duck typing at its best;
these functions accept objects that have certain attributes or methods, and are able to perform generic operations using those methods.
We've used many of the built-in functions already, but let's quickly go through the important ones and pick up a few neat tricks along the way.

#### The `len()` function

#### Reversed

The `reversed()` function takes any sequence as input, and returns a copy of that sequence in reverse order.
It is normally used in for loops when we want to loop over items from back to front.

Similar to `len`, `reversed` calls the `__reversed__()` function on the class for the parameter.
If that method does not exist, `reversed` builds the reversed sequence itself using calls to `__len__` and `__getitem__`, which are used to define a sequence.

#### Enumerate

The for loop doesn't provide us with indexes, but the `enumerate` function gives us something better: it creates a sequence of tuples, where the first object in each tuple is the index and the second is the original item.

#### File I/O

#### Placing it in context

If we run `dir` on a file-like object, we see that it has two special methods named `__enter__` and `__exit__`.
These methods turn the file object into what is known as a **context manager**.
Basically, if we use a special syntax called the with statement, these methods will be called before and after nested code is executed.
On file objects, the `__exit__` method ensures the file is closed, even if an exception is raised.
We no longer have to explicitly manage the closing of the file.

The `with` statement is used in several places in the standard library, where start up or cleanup code needs to be executed.

### An alternative to method overloading

When calling the function, these positional arguments must be specified in order, and none can be missed or skipped.

Any type of object can be passed as an argument: an object, a container, a primitive, even functions and classes.

#### Default arguments

If we want to make an argument optional, rather than creating a second method with a different set of arguments, we can specify a default value in a single method, using an equals sign.
If the calling code does not supply this argument, it will be assigned a default value.
However, the calling code can still choose to override the default by passing in a different value.

With so many options, it may seem hard to pick one, but if you think of the positional arguments as an ordered list, and keyword arguments as sort of like a dictionary, you'll find that the correct layout tends to fall into place.
If you need to require the caller to specify an argument, make it mandatory;
if you have a sensible default, then make it a keyword argument.
Choosing how to call the method normally takes care of itself, depending on which values need to be supplied, and which can be left at their defaults.

#### Variable argument lists

We can also accept arbitrary keyword arguments.
These arrive in the function as a dictionary.
They are specified with two asterisks (as in `**kwargs`) in the function declaration.
This tool is commonly used in configuration setups.
