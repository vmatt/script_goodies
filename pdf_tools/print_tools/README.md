# PDF Print Tools

A collection of utilities for PDF printing and formatting.

## Tools

### print_pdf.py
Converts PDF files to high-quality PNG images and creates printable layouts.

Features:
- High DPI PDF to PNG conversion
- A4 page layout support
- Multiple images per page
- Quality preservation

### a6_to_a4.py
Resizes A6 documents to fit on A4 paper with proper scaling.

Features:
- Maintains aspect ratio
- High-quality scaling
- Proper positioning on A4

## Requirements
```bash
pip install Pillow reportlab pdf2image PyMuPDF
```

## Usage
For print_pdf.py:
```bash
python print_pdf.py
```

For a6_to_a4.py:
```bash
python a6_to_a4.py
```
