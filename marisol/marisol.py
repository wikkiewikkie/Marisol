from PyPDF2 import PdfFileReader, PdfFileWriter

from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes

import copy
import io


class Marisol(object):
    """ A collection of documents to be bates numbered. """
    def __init__(self, prefix, fill, start):
        """
        Base Class

        Args:
            prefix (str): Bates number prefix
            fill (int): Length for zero-filling
            start (int): Starting bates number
        """
        self.prefix = prefix
        self.fill = fill
        self.start = start
        self.index = 0
        self.number = 0

        self.documents = []

    def __len__(self):
        return len(self.documents)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self):
            raise StopIteration
        d = Document(self.documents[self.index],
                     self.prefix,
                     self.fill,
                     self.start+self.number)
        self.index += 1
        self.number += len(d)
        return d

    def append(self, file):
        """
        Add a document to the collection.

        Args:
            file (str or file-like object):  PDF file or file name to add.

        Returns:
            Marisol
        """
        self.documents.append(file)
        return self


class Document(object):
    """
    Class representing documents/files.

    :param file:
    :param prefix:
    :param fill:
    :param start:
    :type file:  File or file-like object
    :type prefix: str
    :type fill: int
    :type start: int
    """
    def __init__(self, file, prefix, fill, start):
        try:
            self.file = io.BytesIO(file.read())
        except TypeError:
            with open(file, "rb") as file:
                self.file = io.BytesIO(file.read())
        self.reader = PdfFileReader(self.file)
        self.prefix = prefix
        self.fill = fill
        self.start = copy.copy(start)
        self.index = 0

    def __len__(self):
        return self.reader.numPages

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self):
            raise StopIteration
        p = Page(self.reader.getPage(self.index),
                 self.prefix,
                 self.fill,
                 self.start+self.index)
        self.index += 1
        return p

    def __str__(self):
        return "{begin} - {end}".format(begin=self.begin, end=self.end)

    @property
    def begin(self):
        num = str(self.start)
        num = num.zfill(self.fill)
        return "{prefix}{num}".format(prefix=self.prefix, num=num)

    @property
    def end(self):
        num = str(self.start+len(self)-1)
        num = num.zfill(self.fill)
        return "{prefix}{num}".format(prefix=self.prefix, num=num)

    def save(self, filename=None):
        filename = filename or "{begin}.pdf".format(begin=self.begin)
        with open(filename, "wb") as out_file:
            writer = PdfFileWriter()
            for page in self:
                page.apply()
                writer.addPage(page.page)
            writer.write(out_file)
        return filename


class Page(object):

    def __init__(self, page, prefix, fill, start):
        self.page = page
        self.prefix = prefix
        self.fill = fill
        self.start = start
        self.height = self.page.mediaBox.upperRight[1]
        self.width = self.page.mediaBox.lowerRight[0]

    def __str__(self):
        return self.number

    def apply(self):
        overlay = Overlay(self.size, self.number)
        self.page.mergePage(overlay.page())

    @property
    def number(self):
        num = str(self.start)
        num = num.zfill(self.fill)
        return "{prefix}{num}".format(prefix=self.prefix, num=num)

    @property
    def size(self):
        dims = (float(self.width), float(self.height))
        for name in dir(pagesizes):
            size = getattr(pagesizes, name)
            if isinstance(size, tuple):
                if dims == size:
                    return name, size
        else:
            return ValueError("Unknown page size.")


class Overlay(object):

    def __init__(self, size, text):
        self.size_name, self.size = size
        self.text = text

        self.output = io.BytesIO()
        self.c = canvas.Canvas(self.output, pagesize=self.size)
        offset_right = 15 # initial offset
        offset_right += len(text)*7  # offset for text length
        self.c.drawString(self.size[0]-offset_right, 15, self.text)
        self.c.showPage()
        self.c.save()

    def page(self):
        self.output.seek(0)
        reader = PdfFileReader(self.output)
        return reader.getPage(0)


