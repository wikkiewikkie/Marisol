# Marisol
[![Build Status](https://travis-ci.org/wikkiewikkie/Marisol.svg?branch=master)](https://travis-ci.org/wikkiewikkie/Marisol)
[![codecov](https://codecov.io/gh/wikkiewikkie/Marisol/branch/master/graph/badge.svg)](https://codecov.io/gh/wikkiewikkie/Marisol)

`Marisol` is a Python library that can be used to add bates numbers to existing PDF files.

## What's a Bates Number?

Bates numbers are identifiers placed on each page in a git stcollection of documents so that they can be uniquely identified.
They are frequently used in the legal field when producing documents in connection with a legal proceeding.  The name
"Bates number" comes from a time when the numbers were stamped on paper documents using a hand stamp that would
increment the number each time it was used.  These hand stamps were invented by Edwin G. *Bates* in 1891 and the name
has stuck, even though the vast majority of these identifiers are now applied electronically.

## Basic Usage

```python
>>> from marisol import Marisol
>>> m = Marisol('TEST', 6, 1)
>>> m.append('first.pdf')  # Path to PDF (1 page)
>>> m.append('second.pdf')  # Path to PDF (3 pages)
>>> m.append(open('first.pdf', 'rb'))  # Marisol can take a file name, or a file object
>>> for doc in m:
>>>     print(doc)
'TEST000001 - TEST000001'
'TEST000002 - TEST000004'
'TEST000005 - TEST000005'
```

## Running Tests

```
py.test --cov=Marisol/ --cov-report=term-missing
```

## License

The [source code](https://github.com/wikkiewikkie/Marisol) for `Marisol` is published under
the [MIT License](https://github.com/wikkiewikkie/Marisol/blob/master/LICENSE).