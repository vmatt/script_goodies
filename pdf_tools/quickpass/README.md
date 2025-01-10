# QuickPass Code Generator

A utility to generate verification code sheets in PDF format.

## Features
- Configurable number of columns and rows
- Customizable number ranges for codes
- Multiple tables per page
- Clean, organized layout
- Professional PDF output

## Requirements
```bash
pip install fpdf
```

## Usage
```bash
python quickpass_v2.py
```

The script will generate a PDF file named "QuickPass_Codes_Cheat_Sheet_Flexible.pdf" containing the verification codes.

## Configuration
You can modify these parameters in the script:
- columns: Number of columns in each table
- column_width: Width of each column
- row_count: Number of rows per table
- ranges: Number ranges for generating codes
