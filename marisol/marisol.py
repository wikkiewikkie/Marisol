from concurrent import futures

from enum import Enum
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes

import copy
import io
import os
import multiprocessing


class Area(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT = 3


class Marisol(object):

    def __init__(self, prefix, fill, start, area=Area.BOTTOM_RIGHT):
        """
        Marisol Base Class - A collection of documents to be bates numbered.

        Args:
            prefix (str): Bates number prefix
            fill (int): Length for zero-filling
            start (int): Starting bates number
            area (Area): Area in which to place the bates number.
        """
        self.prefix = prefix
        self.fill = fill
        self.start = start
        self.area = area

        self.index = 0
        self.number = 0

        self.documents = []
        self.overwrite = False

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
                     self.start+self.number,
                     self.area)
        self.index += 1
        self.number += len(d)
        return d

    def _save_document(self, document):
        """
        Internal method called by thread pool executor.

        Args:
            document (Document):  The document to save.

        Returns:
            (str, bool): The file name saved to and success or failure.
        """
        try:
            filename = document.save(overwrite=self.overwrite)
        except FileExistsError:
            return "EXISTS", False
        else:
            return filename, True

    def append(self, file):
        """
        Add a document to the collection.

        Args:
            file (str or file-like object): PDF file or file name to add.

        Returns:
            marisol.Marisol: The current Marisol instance.
        """
        self.documents.append(file)
        return self

    def save(self, overwrite=False, threads=multiprocessing.cpu_count()*6):
        """Save all documents using a thread pool executor

        Args:
            overwrite (bool, optional): Switch to allow overwriting of existing files.
            threads (int, optional): The number of threads to use when processing.  Defaults to the number of cores
                times six.

        Returns:
            list: each file name and true or false indicating success or failure
        """
        self.overwrite = overwrite
        with futures.ThreadPoolExecutor(threads) as executor:
            results = executor.map(self._save_document, self)
        return list(results)


class Document(object):

    def __init__(self, file, prefix, fill, start, area):
        """
        Represents a document to be numbered.

        Args:
            file (): PDF file associated with this document.
            prefix (str): Bates number prefix.
            fill (int): Length to zero-pad number to.
            start (int): Number to start with.
            area (Area): Area on the document where the number should be drawn
        """
        try:
            self.file = io.BytesIO(file.read())
        except AttributeError:
            with open(file, "rb") as file:
                self.file = io.BytesIO(file.read())
        self.reader = PdfFileReader(self.file)
        self.prefix = prefix
        self.fill = fill
        self.start = copy.copy(start)
        self.area = area

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
                 self.start+self.index,
                 self.area)
        self.index += 1
        return p

    def __str__(self):
        return "{begin} - {end}".format(begin=self.begin, end=self.end)

    @property
    def begin(self):
        """
        Beginning bates number for this document.

        Returns:
            str: Bates number of the first page of the document.
        """
        num = str(self.start)
        num = num.zfill(self.fill)
        return "{prefix}{num}".format(prefix=self.prefix, num=num)

    @property
    def end(self):
        """
        Ending bates number for the document

        Returns:
            str: Bates number of the last page of the document.
        """
        num = str(self.start+len(self)-1)
        num = num.zfill(self.fill)
        return "{prefix}{num}".format(prefix=self.prefix, num=num)

    def save(self, filename=None, overwrite=False):
        """
        Applies the bates numbers and saves to file.

        Args:
            filename (str): Path where the PDF should be saved.
            overwrite (bool): Switch to allow overwriting of existing files.

        Returns:
            str: Path where the file was saved.

        Raises:
            FileExistsError: When the file already exists and overwrite is not enabled.
        """
        filename = filename or "{begin}.pdf".format(begin=self.begin)

        if os.path.exists(filename) and not overwrite:
            raise FileExistsError("PDF file {} already exists and overwrite is disabled.".format(filename))

        with open(filename, "wb") as out_file:
            writer = PdfFileWriter()
            for page in self:
                page.apply()
                writer.addPage(page.page)
            writer.write(out_file)
        return filename


class Page(object):

    def __init__(self, page, prefix, fill, start, area):
        """
        Represents a page within a document that will be bates numbered.

        Args:
            page (PyPdf2.pdf.PageObject): PDF page associated with this page
            prefix (str): Bates number prefix.
            fill (int): Length to zero-pad number to.
            start (int): Number to start with.
            area (Area): Area on the page where the number should be drawn
        """
        self.page = page
        self.prefix = prefix
        self.fill = fill
        self.start = start
        self.area = area

        self.height = self.page.mediaBox.upperRight[1]
        self.width = self.page.mediaBox.lowerRight[0]

    def __str__(self):
        return self.number

    def apply(self):
        """
        Applies the bates number overlay to the page

        Returns:
            bool
        """
        overlay = Overlay(self.size, self.number, self.area)
        self.page.mergePage(overlay.page())
        return True

    @property
    def number(self):
        """
        The bates number for the page.

        Returns:
            str: Bates number.
        """
        num = str(self.start)
        num = num.zfill(self.fill)
        return "{prefix}{num}".format(prefix=self.prefix, num=num)

    @property
    def size(self):
        """
        Takes the dimensions of the original page and returns the name and dimensions of the corresponding ReportLab
        pagesize.

        Returns:
            tuple: name of the page size, and the dimensions (tuple)
        """
        dims = (float(self.width), float(self.height))
        for name in dir(pagesizes):
            size = getattr(pagesizes, name)
            if isinstance(size, tuple):
                if dims == size:
                    return name, size
        else:
            return ValueError("Unknown page size.")


class Overlay(object):

    def __init__(self, size, text, area):
        """
        Overlay that will be used to affix bates numbering

        Args:
            size (tuple): Size of the page as returned by Page.size()
            text: text that will be overlaid on the page.
            area (Area, optional): Area on the overlay where the number should be drawn; defaults to bottom right
        """
        self.size_name, self.size = size
        self.text = text

        self.output = io.BytesIO()
        self.c = canvas.Canvas(self.output, pagesize=self.size)

        position_left, position_bottom = self.position(area)
        self.c.drawString(position_left, position_bottom, self.text)

        self.c.showPage()
        self.c.save()

    def page(self):
        """
        The page used to perform the overlay.

        Returns:
            PyPdf2.pdf.PageObject: The overlay page.
        """
        self.output.seek(0)
        reader = PdfFileReader(self.output)
        return reader.getPage(0)

    def position(self, area):
        """
        Get the appropriate position on the page given an area.

        Args:
            area (Area): Area on the overlay where the number should be drawn

        Returns:
            tuple: the position
        """
        if area in [Area.TOP_LEFT, Area.TOP_RIGHT]:  # top
            from_bottom = self.size[1]-15  # 15 down from height of page
        elif area in [Area.BOTTOM_LEFT, Area.BOTTOM_RIGHT]:  # bottom
            from_bottom = 15  # 15 up from bottom of page
        else:
            raise ValueError("Invalid area {}".format(area))

        if area in [Area.TOP_LEFT, Area.BOTTOM_LEFT]:  # left
            from_left = 15
        elif area in [Area.TOP_RIGHT, Area.BOTTOM_RIGHT]:  # right
            offset = 15  # initial offset
            offset += len(self.text) * 7  # offset for text length
            from_left = self.size[0]-offset

        return from_left, from_bottom
