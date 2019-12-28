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
