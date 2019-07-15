# pyenv

## Overview

pyenv lets you easily switch between multiple versions of Python.

## Installation

```bash
brew install pyenv
```

## Usage

```bash
pyenv versions

pyenv install -l

pyenv install 3.7.4

pyenv global 3.7.4

echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
```

## References

[https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)
