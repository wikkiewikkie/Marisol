# Marisol
[![Build Status](https://travis-ci.org/wikkiewikkie/Marisol.svg?branch=master)](https://travis-ci.org/wikkiewikkie/Marisol)
[![codecov](https://codecov.io/gh/wikkiewikkie/Marisol/branch/master/graph/badge.svg)](https://codecov.io/gh/wikkiewikkie/Marisol)

`Marisol` is a Python library that can be used to add bates numbers to existing PDF files.

## What's a Bates Number?

Bates numbers are identifiers placed on each page in a collection of documents so that they can be uniquely identified.
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

## Testing

`Marisol` is automatically tested against Python versions 3.2 - 3.6.  Tests can be run manually using `pytest`.

```
py.test --cov=Marisol/ --cov-report=term-missing
```

## Performance

Page-per-second performance can be measured using the `run_benchmark.py` script in the `benchmark` folder.

```
python run_benchmark.py
Creating test files...
Starting Benchmark...
Benchmark Complete.
17.691006240916472 seconds elapsed.
56.525897192165345 pages per second.
Cleaning up...
```
On a laptop with an AMD A10-8700B processor and SSD hard drive, `Elizabeth` is currently capable of bates-numbering
about 56 pages per second.

## License

The [source code](https://github.com/wikkiewikkie/Marisol) for `Marisol` is published under
the [MIT License](https://github.com/wikkiewikkie/Marisol/blob/master/LICENSE).