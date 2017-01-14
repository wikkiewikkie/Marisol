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

## Usage

```python
>>> from marisol import Marisol
>>> m = Marisol('TEST', 6, 1)  # Begin numbering with TEST000001
>>> m.append('first.pdf')  # Path to PDF (1 page)
>>> m.append('second.pdf')  # Path to PDF (3 pages)
>>> m.save()  # Export numbered PDFs, named for the bates number.
```

### Loading

Documents can be loaded using a file name or by passing a file-like object.

```python
>>> m.append('myPdf.pdf')  # Load by file name
>>> m.append(open('myOtherPdf.pdf', 'rb'))  # Load with a file object
```

### Exporting

Exports can be performed at the document-level, or against all documents using the `save()` method.  When a file name
is not specified, the resulting PDFs will be named for the beginning bates number of that document.

```python
>>> m.save()  # save all documents
>>> doc = next(m)
>>> doc.save()  # save one document
>>> another_doc = next(m)
>>> another_doc.save("customName.pdf")  # specify a custom file name
```

## Testing

`Marisol` is automatically tested against Python versions 3.2 - 3.6.  Tests can be run manually using `pytest`.

```
py.test --cov=marisol/ --cov-report=term-missing
```

## Performance

Page-per-second performance can be measured using the `run_benchmark.py` script in the `benchmark` folder.

```
python run_benchmark.py
Creating test files...
Starting Benchmark...
Benchmark Complete.
34.294837610624 seconds elapsed.
145.794537847617 pages per second.
Cleaning up...
```
On a workstation with a dual-core Pentium G3258 CPU and SSD hard drive, `Marisol` is currently capable of
bates-numbering over 140 pages per second.  `Marisol` uses multiple threads during processing and performance is
CPU-bound, so a faster processor with additional cores will result in better performance.

## License

The [source code](https://github.com/wikkiewikkie/Marisol) for `Marisol` is published under
the [MIT License](https://github.com/wikkiewikkie/Marisol/blob/master/LICENSE).