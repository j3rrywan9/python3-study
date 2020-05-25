# Built-in Types

## 2.7

## 3.8

### Iterator Types

#### Generator Types

Python's generators provide a convenient way to implement the iterator protocol.
If a container object's `__iter__()` method is implemented as a generator, it will automatically return an iterator object (technically, a generator object) supplying the `__iter__()` and `__next__()` methods.

### Sequence Types - list, tuple, range

### Text Sequence Type - str

Since there is no separate "character" type, indexing a string produces strings of length 1.
That is, for a non-empty string *s*, `s[0] == s[0:1]`.

#### String Methods

Strings implement all of the common sequence operations, along with the additional methods described below.

```python
str.isalnum()
```
Return `True` if all characters in the string are alphanumeric and there is at least one character, `False` otherwise.

```python
str.isdigit()
```
Return `True` if all characters in the string are digits and there is at least one character, `False` otherwise.

```python
str.lower()
```
Return a copy of the string with all the cased characters converted to lowercase.

```python
str.split(sep=None, maxsplit=-1)
```
Return a list of the words in the string, using `sep` as the delimiter string.
If `maxsplit` is given, at most `maxsplit` splits are done (thus, the list will have at most `maxsplit+1` elements). 
If `maxsplit` is not specified or `-1`, then there is no limit on the number of splits (all possible splits are made).
