# re - Regular Expression Operations

## 3.8

This module provides regular expression matching operations similar to those found in Perl.

### Regular Expression Syntax

A regular expression (or RE) specifies a set of strings that matches it;
the functions in this module let you check if a particular string matches a given regular expression (or if a given regular expression matches a particular string, which comes down to the same thing).

Regular expressions can contain both special and ordinary characters.

The special characters are:

`(...)`

Matches whatever regular expression is inside the parentheses, and indicates the start and end of a group;
the contents of a group can be retrieved after a match has been performed, and can be matched later in the string with the `\number` special sequence, described below.
To match the literals `'('` or `')'`, use `\(` or `\)`, or enclose them inside a character class: `[(]`, `[)]`.

### Module Contents

The module defines several functions, constants, and an exception.
Some of the functions are simplified versions of the full featured methods for compiled regular expressions.
Most non-trivial applications always use the compiled form.

```python
re.search(pattern, string, flags=0)
```
Scan through *string* looking for the first location where this regular expression produces a match, and return a corresponding match object.
Return `None` if no position in the string matches the pattern;
note that this is different from finding a zero-length match at some point in the string.

```python
re.match(pattern, string, flags=0)
```

### Regular Expression Objects

### Match Objects

Match objects always have a boolean value of `True`.
Since `match()` and `search()` return `None` when there is no match, you can test whether there was a match with a simple `if` statement:
```python
match = re.search(pattern, string)
if match:
    process(match)
```
Match objects support the following methods and attributes:
```python
Match.group([group1, ...])
```
Returns one or more subgroups of the match.

```python
Match.groups(default=None)
```
Return a tuple containing all the subgroups of the match, from 1 up to however many groups are in the pattern.
The `default` argument is used for groups that did not participate in the match;
it defaults to `None`.
