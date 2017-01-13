# Marisol
Library for bates numbering PDF files.

## Basic Usage

```python
>>> from marisol import Marisol
>>> m = Marisol("TEST", 6, 1)
>>> m.append("first.pdf")  # Path to PDF (1 page)
>>> m.append("second.pdf")  # Path to PDF (3 pages)
>>> m.append(open("first.pdf", "rb"))  # Marisol can take a file name, or a file object
>>> for doc in m:
>>>     print(doc)
'TEST000001 - TEST000001'
'TEST000002 - TEST000004'
'TEST000005 - TEST000005'
```