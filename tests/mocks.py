from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes

import io


class MockPDF(object):
    """
    Mocks a PDF of n pages.
    """
    def __init__(self, pages, size=pagesizes.letter):
        """
        Init

        Args:
            pages (int): Number of pages to mock.
        """
        self.pages = pages
        self.size = size

        self.file = io.BytesIO()

        canvas = Canvas(self.file, pagesize=self.size)

        for page_num in range(pages):
            canvas.drawString(30, self.size[1]-30, "MockPDF Created By Marisol")
            canvas.drawString(30, self.size[1]-60, "Page {} of {}".format(page_num+1, pages))
            canvas.drawString(30, self.size[1]-90, "Dimensions: {}".format(size))
            canvas.showPage()

        canvas.save()

    def read(self):
        self.file.seek(0)
        return self.file.read()
