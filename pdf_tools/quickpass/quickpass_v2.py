from fpdf import FPDF
import random

class PDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4', columns=4, column_width=10, row_count=24, ranges=None):
        super().__init__(orientation, unit, format)
        self.columns = columns
        self.column_width = column_width
        self.row_count = row_count
        self.ranges = ranges if ranges else [(1000, 9999), (10, 99), (10, 99), (10, 99)]

    def header(self):
        self.set_font('Arial', 'B', 12)

    def cheat_sheet_table(self, cheat_sheet, start_x, start_y):
        self.set_xy(start_x, start_y)
        header = [str(i + 1) for i in range(self.columns)]

        # Add table header
        self.set_font('Arial', 'B', 10)
        for i, header_text in enumerate(header):
            self.cell(self.column_width, 10, header_text, 1, 0, 'C')
        self.ln()

        # Add table rows
        self.set_xy(start_x, self.get_y())
        self.set_font('Arial', '', 10)
        for row in cheat_sheet:
            for i, item in enumerate(row):
                self.cell(self.column_width, 10, str(item), 1, 0, 'C')
            self.ln()
            self.set_x(start_x)

    def generate_verification_matrix(self):
        cheat_sheet = []
        for _ in range(self.row_count):
            row = []
            for start, end in self.ranges:
                row.append(random.randint(start, end))
            cheat_sheet.append(tuple(row))
        return sorted(cheat_sheet, key=lambda x: x)


# Parameters
columns = 4
column_width = 10
row_count = 5
ranges = [(1000, 9999), (10, 99), (10, 99), (10, 99)]

# Create instance of PDF class with custom parameters
pdf = PDF(columns=columns, column_width=column_width, row_count=row_count, ranges=ranges)

# Generate the cheat sheet
cheat_sheet = pdf.generate_verification_matrix()

# Page and table sizes
page_width = 210
page_height = 297
table_height = 10 * (len(cheat_sheet) // pdf.columns + 1)
max_tables_per_row = page_width // (columns * column_width + 10)
max_rows_per_page = page_height // (table_height + 10)

# Add pages and tables
tables_needed = 4
tables_added = 0

while tables_added < tables_needed:
    pdf.add_page()
    for row in range(max_rows_per_page):
        for col in range(max_tables_per_row):
            if tables_added >= tables_needed:
                break
            start_x = 10 + col * (columns * column_width + 10)
            start_y = 10 + row * (table_height + 10)
            pdf.cheat_sheet_table(cheat_sheet, start_x, start_y)
            tables_added += 1
        if tables_added >= tables_needed:
            break

# Save the PDF to a file
pdf_file_path = "QuickPass_Codes_Cheat_Sheet_Flexible.pdf"
pdf.output(pdf_file_path)
