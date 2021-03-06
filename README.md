# Marisol
[![Build Status](https://travis-ci.org/wikkiewikkie/Marisol.svg?branch=master)](https://travis-ci.org/wikkiewikkie/Marisol)
[![codecov](https://codecov.io/gh/wikkiewikkie/Marisol/branch/master/graph/badge.svg)](https://codecov.io/gh/wikkiewikkie/Marisol)

`Marisol` is a Python library that can be used to add bates numbers, static text, and redactions to existing PDF files.

## What's a Bates Number?

Bates numbers are identifiers placed on each page in a collection of documents so that they can be uniquely identified.
They are frequently used in the legal field when producing documents in connection with a legal proceeding.  The name
"Bates number" comes from a time when the numbers were stamped on paper documents using a hand stamp that would
increment the number each time it was used.  These hand stamps were invented by Edwin G. *Bates* in 1891 and the name
has stuck, even though the vast majority of these identifiers are now applied electronically.

## Installation

To install `Marisol`, simply:

```
pip install Marisol
```

`Marisol` requires the [pypdf2](https://github.com/mstamy2/PyPDF2) and [reportlab](https://pypi.python.org/pypi/reportlab) libraries, as well as any associated dependencies.

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

### Areas

Bates numbers can be placed in four different areas on the page. Top-left, top-right, bottom-right, and bottom-left.
To set the area, simply specify it when calling `Marisol`.  If no area is specified, the bates number will be placed
in the bottom-right.

```python
>>> from marisol import Area, Marisol
>>> m = Marisol("TEST", 6, 1, area=Area.TOP_LEFT)
```

### Static Text

Static text overlays are used when you want to apply the same text to every page in a document.  Since the text may
change between documents, it is applied at the document level using a `StaticOverlay`.

```python
>>> from marisol import Area, Marisol
>>> m = Marisol("TEST", 6, 1)
>>> m.append('myPdf.pdf')
>>> overlay = StaticOverlay("CONFIDENTIAL")
>>> doc = m[0]
>>> doc.add_overlay(overlay, Area.BOTTOM_LEFT)
```

These overlays may be applied to any of the defined areas, but each may contain only be one `StaticOverlay`.  A
`StaticOverlay` can not occupy the same area as the bates number.

### Redaction

To draw a redaction on a page, you must first create a `Redaction` object and specify a location and size for it.  Then
apply the redaction to a `Page` object using the `add_redaction()` method.  When creating the `Redaction` object, you
may also include some text to draw inside the redaction box and a `RedactionStyle`.  If no text or style is specified,
the redaction will be drawn as a solid black box with no text.

```python
>>> from marisol import Marisol, Redaction, RedactionStyle
>>> m = Marisol("TEST", 6, 1)
>>> m.append('myPdf.pdf')
>>> doc = m[0]
>>> first_page = doc[0]
>>> location = (144, 216)  # offset from the left and bottom of the page.
>>> size = (72, 36)  # width and height of the redaction
>>> redaction = Redaction(location, size)  # create a plain redaction
>>> first_page.add_redaction(redaction)  # add the redaction to the page
>>> second_page = doc[1]
>>> another_redaction = Redaction(location, size, "PRIVILEGED", RedactionStyle.OUTLINE) # with text and a style
>>> second_page.add_redaction(another_redaction)
```

Page positions and dimensions are specified in points (1/72nd of an inch).  The example above draws a redaction where
the bottom-left corner is 2 inches from the left of the page and 3 inches from the bottom of the page. It is one inch
wide and 1/2 inches tall.

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

`Marisol` is automatically tested against the development and production branches of Python 3.4 - 3.7.  Tests can be
run manually using `pytest`.

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