from marisol import Area, Document, Marisol, OutsideBoundariesError, Page, Redaction, RedactionStyle, StaticOverlay
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
    with open("test.pdf", "wb") as test_file:
        p = MockPDF(5)
        test_file.write(p.read())

    # append from open file
    empty.append(MockPDF(1)).append(MockPDF(3))
    assert len(empty) == 2
    empty.append(MockPDF(5))
    assert len(empty) == 3

    # append from file name
    empty.append("test.pdf")
    assert len(empty) == 4

    for doc in empty:
        assert isinstance(doc, Document)

    os.remove("test.pdf")


def test_marisol_getitem(populated):
    assert isinstance(populated[0], Document)


def test_marisol_iteration(populated):
    assert len(populated) == 3  # instance contains three documents
    count = 0
    for doc in populated:
        assert isinstance(doc, Document)
        count += 1
    assert count == 3


def test_marisol_save(populated):
    result = populated.save()
    file_names = []
    for filename, success in result:
        assert success
        file_names.append(filename)

    result = populated.save()
    for filename, success in result:
        assert not success  # should fail because files exists already

    result = populated.save(overwrite=True)
    for filename, success in result:
        assert success  # should succeed because overwrite is enabled

    for filename in file_names:  # clean up
        os.remove(filename)


def test_document_add_overlay(document):
    bl_overlay = StaticOverlay("TESTLEGEND", Area.BOTTOM_LEFT)
    document.add_overlay(bl_overlay)
    assert isinstance(document.overlays[Area.BOTTOM_LEFT], StaticOverlay)
    br_overlay = StaticOverlay("ANOTHER", Area.BOTTOM_RIGHT)
    with pytest.raises(ValueError):
        document.add_overlay(br_overlay)  # conflicts with bates area
    document.save("STATIC.pdf")
    os.remove("STATIC.pdf")


def test_document_iteration(document):
    assert len(document) == 3  # document contains three pages
    count = 0
    for p in document:
        assert isinstance(p, Page)
        count += 1
    assert count == 3


def test_document_save(document):
    filename = document.save()
    assert filename == "TEST000002.pdf"  # will automatically use begin bates for file name
    assert os.path.exists(filename)  # file is written to disk
    with pytest.raises(FileExistsError):
        document.save()  # file already exists
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


def test_page_str(page):
    assert str(page) == "TEST000003"


def test_page_apply(page):
    assert page.apply()


def test_redaction_default(document):
    p = document[0]
    r = Redaction((100, 200),  (200, 200), "BLAH")
    p.add_redaction(r)
    document.save("redaction_default.pdf", overwrite=True)
    os.remove("redaction_default.pdf")


def test_redaction_error(document):
    """Check that redactions drawn outside of dimensions raise an error"""
    p = document[0]
    r = Redaction((1000, 200),  (200, 200), "BLAH")

    with pytest.raises(OutsideBoundariesError):
        p.add_redaction(r)


def test_redaction_styled(document):
    p = document[0]
    r = Redaction((100, 200), (200, 50), "TEST", RedactionStyle.OUTLINE)
    p.add_redaction(r)
    document.save("redaction_styled.pdf")
    os.remove("redaction_styled.pdf")
