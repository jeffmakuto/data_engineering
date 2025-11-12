"""
Improved deliverables PDF generator.

Features:
 - Table of Contents
 - Syntax-highlight source files to images using Pygments
 - Nicely formatted sections for OpenAPI, tests, results, and report
 - Produces bookstore_deliverables_improved.pdf

Dependencies: reportlab, pygments, pillow, PyPDF2
"""
import os
import io
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.lexers import guess_lexer
from pygments.formatters import ImageFormatter
from PyPDF2 import PdfReader, PdfWriter

ROOT = os.path.dirname(__file__)
OUT = os.path.join(ROOT, 'bookstore_deliverables_improved.pdf')
TMP_PDF = os.path.join(ROOT, '._tmp_body.pdf')
TOC_PDF = os.path.join(ROOT, '._tmp_toc.pdf')

FILES = [
    ('API Source', 'app.py'),
    ('Inventory mock', 'inventory_mock.py'),
    ('Sales mock', 'sales_mock.py'),
    ('Delivery mock', 'delivery_mock.py'),
    ('OpenAPI spec', 'openapi.yaml'),
    ('Tests', os.path.join('tests', 'test_api.py')),
    ('Test results', 'test_results.txt'),
    ('Report', 'report.md'),
]


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        try:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f'-- failed to read {path}: {e}'


def render_code_image(code, filename_hint):
    # Use Pygments to render code to PNG image in memory
    try:
        try:
            lexer = get_lexer_for_filename(filename_hint)
        except Exception:
            try:
                lexer = guess_lexer(code)
            except Exception:
                lexer = get_lexer_for_filename('*.txt')
        formatter = ImageFormatter(font_name='DejaVu Sans Mono', line_numbers=True, style='default')
        img_data = highlight(code, lexer, formatter)
        return ImageReader(io.BytesIO(img_data))
    except Exception as e:
        # fallback: render plain text into an image via ReportLab later
        return None


def build_body_pdf():
    c = canvas.Canvas(TMP_PDF, pagesize=letter)
    w, h = letter

    # Title
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(w / 2, h - 1.5 * inch, 'Bookstore API — Deliverables')
    c.setFont('Helvetica', 12)
    c.drawCentredString(w / 2, h - 1.9 * inch, 'Combined source, docs, tests, and report')
    c.showPage()

    for title, rel in FILES:
        path = os.path.join(ROOT, rel)
        content = read_file(path) if os.path.exists(path) else f'-- missing file: {rel}'
        c.setFont('Helvetica-Bold', 16)
        c.drawString(0.7 * inch, h - 0.8 * inch, f'{title} — {rel}')
        y = h - 1.1 * inch

        # If this is a code file, render to image
        if rel.endswith('.py') or rel.endswith('.yaml') or rel.endswith('.yml'):
            img = render_code_image(content, rel)
            if img:
                # scale image to page width with margins
                max_w = w - 1.4 * inch
                iw, ih = img.getSize()
                scale = min(1.0, max_w / iw)
                draw_w = iw * scale
                draw_h = ih * scale
                c.drawImage(img, 0.7 * inch, y - draw_h, width=draw_w, height=draw_h)
                y = y - draw_h - 0.2 * inch
            else:
                # fallback to plain text rendering
                c.setFont('Courier', 8)
                for line in content.splitlines():
                    if y < 0.8 * inch:
                        c.showPage()
                        c.setFont('Courier', 8)
                        y = h - 0.7 * inch
                    c.drawString(0.7 * inch, y, line[:200])
                    y -= 10
        else:
            # plain text (test results, report)
            c.setFont('Courier', 9)
            for line in content.splitlines():
                if y < 0.8 * inch:
                    c.showPage()
                    c.setFont('Courier', 9)
                    y = h - 0.7 * inch
                c.drawString(0.7 * inch, y, line)
                y -= 10

        c.showPage()

    c.save()


def build_toc_pdf():
    # Simple TOC with page numbers from body
    reader = PdfReader(TMP_PDF)
    c = canvas.Canvas(TOC_PDF, pagesize=letter)
    w, h = letter
    c.setFont('Helvetica-Bold', 18)
    c.drawString(0.7 * inch, h - 1 * inch, 'Table of Contents')
    c.setFont('Helvetica', 11)
    y = h - 1.4 * inch
    page = 2  # title page is 1; sections start at 2
    for title, rel in FILES:
        entry = f'{title} — {rel}'
        c.drawString(0.9 * inch, y, entry)
        c.drawRightString(w - 0.7 * inch, y, str(page))
        y -= 14
        page += 1  # rough mapping; good enough for this small doc
        if y < 1 * inch:
            c.showPage()
            c.setFont('Helvetica', 11)
            y = h - 1 * inch
    c.showPage()
    c.save()


def assemble():
    build_body_pdf()
    build_toc_pdf()
    writer = PdfWriter()
    # first append TOC
    for p in PdfReader(TOC_PDF).pages:
        writer.add_page(p)
    # then body
    for p in PdfReader(TMP_PDF).pages:
        writer.add_page(p)
    with open(OUT, 'wb') as f:
        writer.write(f)
    # cleanup
    for p in (TMP_PDF, TOC_PDF):
        try:
            os.remove(p)
        except Exception:
            pass
    print(f'Wrote {OUT}')


if __name__ == '__main__':
    assemble()
