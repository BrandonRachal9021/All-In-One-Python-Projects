md2pdf - simple Markdown to PDF converter

Usage

1. Create a virtualenv (recommended):

   python3 -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. Convert a file:

   python convert.py input.md output.pdf

Notes

- This uses `markdown` + `xhtml2pdf`. For complex CSS or better typography, use
  `weasyprint` or `pandoc` with a LaTeX engine.

- The script is minimal; it doesn't support images with relative paths or
  advanced styling.
