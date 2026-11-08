"""Tests for attachment extraction and vision gating."""
from io import BytesIO

import pytest
from docx import Document
from openpyxl import Workbook
from pptx import Presentation
from pypdf import PdfWriter

import attachments


class FakeUpload:
    def __init__(self, name, data):
        self.name = name
        self._data = data

    def getvalue(self):
        return self._data


def test_text_attachment_extraction():
    u = FakeUpload('notes.md', '# Title\nhello'.encode())
    assert attachments.extract_uploaded_file(u) == '# Title\nhello'


def test_empty_pdf_extracts_without_error():
    w = PdfWriter()
    w.add_blank_page(width=200, height=200)
    buf = BytesIO()
    w.write(buf)
    assert attachments.extract_uploaded_file(FakeUpload('blank.pdf', buf.getvalue())) == ''


def test_docx_with_table():
    d = Document()
    d.add_paragraph('body text')
    t = d.add_table(rows=1, cols=2)
    t.rows[0].cells[0].text = 'c1'
    t.rows[0].cells[1].text = 'c2'
    buf = BytesIO()
    d.save(buf)
    out = attachments.extract_uploaded_file(FakeUpload('a.docx', buf.getvalue()))
    assert 'body text' in out and 'c1\tc2' in out


def test_xlsx_worksheet():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Data'
    ws.append(['name', 'qty'])
    ws.append(['peas', 42])
    buf = BytesIO()
    wb.save(buf)
    out = attachments.extract_uploaded_file(FakeUpload('a.xlsx', buf.getvalue()))
    assert '### Worksheet: Data' in out
    assert 'peas\t42' in out


def test_pptx_slides():
    prs = Presentation()
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = 'Hello deck'
    buf = BytesIO()
    prs.save(buf)
    out = attachments.extract_uploaded_file(FakeUpload('a.pptx', buf.getvalue()))
    assert '### Slide 1' in out and 'Hello deck' in out


def test_unsupported_extension_rejected():
    with pytest.raises(ValueError, match='Unsupported'):
        attachments.extract_uploaded_file(FakeUpload('evil.exe', b'MZ'))


def test_non_utf8_text_does_not_crash():
    u = FakeUpload('latin.txt', b'caf\xe9')
    assert 'caf' in attachments.extract_uploaded_file(u)


def test_image_rejected_for_non_vision_model():
    img = FakeUpload('shot.png', b'\x89PNG\r\n\x1a\nfake')
    with pytest.raises(ValueError, match='vision'):
        attachments.build_user_content('describe', [img], supports_vision=False)


def test_image_accepted_for_vision_model():
    img = FakeUpload('shot.jpg', b'\xff\xd8\xfffake')
    msg, images = attachments.build_user_content('describe', [img], supports_vision=True)
    assert msg == 'describe'
    assert images[0]['media_type'] == 'image/jpeg'


def test_extraction_is_capped():
    big = FakeUpload('big.txt', b'x' * (attachments.MAX_EXTRACTED_CHARS + 10_000))
    msg, _ = attachments.build_user_content('prompt', [big], supports_vision=False)
    assert len(msg) <= attachments.MAX_EXTRACTED_CHARS + len('prompt') + 100
