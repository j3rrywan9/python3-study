# Built-in Functions

## 2.7

### `abs(x)`

### `all(iterable)`

### `any(iterable)`

### `cmp(x, y)`

Compare the two objects x and y and return an integer according to the outcome.
The return value is negative if x < y, zero if x == y and strictly positive if x > y.

### `dir([object])`

Without arguments, return the list of names in the current local scope.
With an argument, attempt to return a list of valid attributes for that object.

If the object has a method named `__dir__()`, this method will be called and must return the list of attributes.
This allows objects that implement a custom `__getattr__()` or `__getattribute__()` function to customize the way `dir()` reports their attributes.

If the object does not provide `__dir__()`, the function tries its best to gather information from the object's `__dict__` attribute, if defined, and from its type object.
The resulting list is not necessarily complete, and may be inaccurate when the object has a custom `__getattr__()`.

The default `dir()` mechanism behaves differently with different types of objects, as it attempts to produce the most relevant, rather than complete, information:
* If the object is a module object, the list contains the names of the module's attributes.
* If the object is a type or class object, the list contains the names of its attributes, and recursively of the attributes of its bases.
* Otherwise, the list contains the object's attributes' names, the names of its class's attributes, and recursively of the attributes of its class's base classes.

The resulting list is sorted alphabetically.

### `filter(function, iterable)`

### `getattr(object, name[, default])`

### `hasattr(object, name)`

### `isinstance(object, classinfo)`

### `issubclass(class, classinfo)`

### `len(s)`

Return the length (the number of items) of an object.
The argument may be a sequence (such as a string, bytes, tuple, list, or range) or a collection (such as a dictionary, set, or frozen set).

### `map(function, iterable, ...)`

Apply *function* to every item of *iterable* and return a list of the results.

### `range(stop)`

### `range(start, stop[, step])`

### `xrange(stop)`

### `xrange(start, stop[, step])`