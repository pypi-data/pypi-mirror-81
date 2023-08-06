[![PyPI version](https://badge.fury.io/py/munch-stubs.svg)](https://pypi.org/project/munch-stubs)
[![Code on Github](https://img.shields.io/badge/Code-GitHub-brightgreen)](https://github.com/MartinThoma/munch-stubs)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub last commit](https://img.shields.io/github/last-commit/MartinThoma/munch-stubs)

# munch-stubs

Add types for [munch](https://pypi.org/project/munch/) for mypy.

## Installation

```
$ pip install munch-stubs
```

## Usage

Mypy will automatically use the type annotations in this package, once it is
installed. You just need to annotate your code:

```python
from munch import Munch


def foo(bar: Munch) -> int:
    return bar.foo
```

For general hints how to use type annotations, please read [Type Annotations in Python 3.8](https://medium.com/analytics-vidhya/type-annotations-in-python-3-8-3b401384403d).
