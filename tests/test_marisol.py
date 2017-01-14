from marisol import Document, Marisol, Overlay, Page
from PyPDF2.pdf import PageObject
from tests.mocks import MockPDF

import os
import pytest


@pytest.fixture
def empty():
    """empty instance"""
    return Marisol("TEST", 6, 1)


@pytest.fixture
def populated(empty):
    """instance containing three documents"""
    empty.append(MockPDF(1))
    empty.append(MockPDF(3))
    empty.append(MockPDF(5))
    return empty


@pytest.fixture
def document(populated):
    """second document, containing three pages"""
    next(populated)
    return next(populated)


@pytest.fixture
def page(document):
    """ second page of three page document """
    next(document)
    return next(document)


def test_marisol_append(empty):
    # append from file name
    with open("test.pdf", "wb") as test_file:
        p = MockPDF(5)
        test_file.write(p.read())

    empty.append("test.pdf")
    assert len(empty) == 1
    os.remove("test.pdf")

    # append from open file
    empty.append(MockPDF(1)).append(MockPDF(3))
    assert len(empty) == 3
    empty.append(MockPDF(5))
    assert len(empty) == 4


def test_marisol_iteration(populated):
    assert len(populated) == 3  # instance contains three documents
    count = 0
    for doc in populated:
        assert isinstance(doc, Document)
        count += 1
    assert count == 3


def test_document_iteration(document):
    assert len(document) == 3  # document contains three pages
    count = 0
    for page in document:
        assert isinstance(page, Page)
        count += 1
    assert count == 3


def test_document_save(document):
    filename = document.save()
    assert filename == "TEST000002.pdf"  # will automatically use begin bates for file name
    assert os.path.exists(filename)  # file is written to disk
    os.remove(filename)

    filename = document.save("ANOTHER.pdf")
    assert filename == "ANOTHER.pdf"  # file name can be overridden
    assert os.path.exists(filename)  # file is written to disk
    os.remove("ANOTHER.pdf")


def test_document_str(populated):
    doc = next(populated)
    assert str(doc) == "TEST000001 - TEST000001"  # first document has one page
    doc = next(populated)
    assert str(doc) == "TEST000002 - TEST000004"  # second document has three pages


def test_overlay(page):
    o = Overlay(page.size, page.number)
    assert isinstance(o.page(), PageObject)


def test_page_str(page):
    assert str(page) == "TEST000003"


def test_page_apply(page):
    page.apply()