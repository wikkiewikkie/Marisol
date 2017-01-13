from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes

import io


class MockPDF(object):
    """
    Mocks a PDF of n pages.
    """
    def __init__(self, pages):
        """
        Init

        Args:
            pages (int): Number of pages to mock.
        """
        self.pages = pages

        self.file = io.BytesIO()

        canvas = Canvas(self.file, pagesize=pagesizes.letter)

        for page_num in range(pages):
            canvas.drawString(200, 200, "MockPDF {}".format(page_num))
            canvas.showPage()

        canvas.save()

    def read(self):
        self.file.seek(0)
        return self.file.read()
