from PyPDF2 import PdfFileReader, PdfFileWriter

from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes

import copy
import io


class Marisol(object):

    def __init__(self, prefix, fill, start):
        """
        Base Class

        :param prefix: Bates number prefix.
        :param fill: Number of digits for zero-filling
        :param start: Beginning number.
        :type prefix: str
        :type fill: int
        :type start: int
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

    def add_documents(self, file_names):
        for file_name in file_names:
            self.documents.append(file_name)

    def run(self):
        for document in self.documents:
            with open(document, "rb") as file:
                print(self.prefix, self.fill, self.index)
                d = Document(file, self.prefix, self.fill, self.index)
                self.index += len(d)


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
        return "{prefix}{start} - {prefix}{end}".format(prefix=self.prefix,
                                                        start=str(self.start).zfill(self.fill),
                                                        end=str(self.start+len(self)-1).zfill(self.fill))

    def save(self):
        with open("out.pdf", "wb") as out_file:
            writer = PdfFileWriter()
            for page in self.reader.pages:
                p = Page(page)
                p.apply()
                writer.addPage(p.page)
            writer.write(out_file)


class Page(object):

    def __init__(self, page, prefix, fill, start):
        self.page = page
        self.prefix = prefix
        self.fill = fill
        self.start = start
        self.height = self.page.mediaBox.upperRight[1]
        self.width = self.page.mediaBox.lowerRight[0]

        #self.overlay = Overlay(self.page_size()[0])

    def __str__(self):
        return "{prefix}{number}".format(prefix=self.prefix,
                                         number=str(self.start).zfill(self.fill))

    def apply(self):
        with open("temp.pdf", "rb") as temp_file:
            overlay_pdf = PdfFileReader(temp_file)
            overlay_page = overlay_pdf.getPage(0)

            # read your existing PDF
            self.page.mergePage(overlay_page)

    @property
    def number(self):
        return "{}{}".format(self.prefix, str(self.start).zfill(self.fill))

    def page_size(self):
        dims = (float(self.width), float(self.height))
        for name in dir(pagesizes):
            size = getattr(pagesizes, name)
            if isinstance(size, tuple):
                if dims == size:
                    return name, size
        else:
            return ValueError("Unknown page size.")


class Overlay(object):

    def __init__(self, size):
        # self.output = io.BytesIO()
        self.output = open("temp.pdf", "wb")
        self.c = canvas.Canvas("temp.pdf", pagesize=pagesizes.letter)
        self.add_bates()
        self.c.save()

    def add_bates(self):
        self.c.drawString(10, 100, "Hello world")

    def save(self):
        self.c.save()

    def file(self):
        pass


