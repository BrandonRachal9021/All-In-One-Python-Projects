#!/usr/bin/env python3
"""Simple CLI: convert Markdown to PDF.

Usage:
    python convert.py input.md output.pdf

This script converts Markdown to HTML using the `markdown` package, then renders
HTML to PDF using `xhtml2pdf` (pisa).

It's intentionally minimal; for more advanced needs consider `pandoc` or
`weasyprint`.
"""
import sys
import os
from markdown import markdown
from xhtml2pdf import pisa


def md_to_html(md_text: str) -> str:
    """Convert markdown text to basic HTML with UTF-8 meta."""
    html_body = markdown(md_text, extensions=["extra", "tables", "toc"])
    html = (
        "<!DOCTYPE html>\n"
        "<html><head>\n"
        "<meta charset=\"utf-8\">\n"
        "<style>body{font-family: Arial, Helvetica, sans-serif; padding:24px; line-height:1.4}</style>\n"
        "</head><body>\n"
        f"{html_body}\n"
        "</body></html>"
    )
    return html


def html_to_pdf(html: str, output_path: str) -> bool:
    """Render HTML string to a PDF file. Returns True on success."""
    with open(output_path, "wb") as out_file:
        pisa_status = pisa.CreatePDF(src=html, dest=out_file)
    return not pisa_status.err


def main(argv):
    if len(argv) != 3:
        print("Usage: convert.py input.md output.pdf")
        return 2

    input_path = argv[1]
    output_path = argv[2]

    if not os.path.isfile(input_path):
        print(f"Input file not found: {input_path}")
        return 3

    with open(input_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = md_to_html(md_text)
    ok = html_to_pdf(html, output_path)
    if not ok:
        print("Failed to create PDF (xhtml2pdf error)")
        return 4

    print(f"Wrote PDF: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
