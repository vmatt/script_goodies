from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pdf2image import convert_from_path

def convert_pdf_to_png(pdf_file, dpi=600):
    images = convert_from_path(pdf_file, dpi=dpi)
    for i, image in enumerate(images):
        image.save(f"page_{i+1}.png", "PNG")

# Example usage
pdf_file = "page.pdf"  # replace with your PDF file name
convert_pdf_to_png(pdf_file)


def create_pdf(input_image1, input_image2, output_pdf, dpi=300):
    # Convert DPI to a scale factor for reportlab (default is 72 DPI)
    scale = dpi / 72.0
    width, height = A4
    # Adjust the page size to the new DPI
    adjusted_page_width = width * scale
    adjusted_page_height = height * scale

    # Create canvas with adjusted sizes and DPI
    c = canvas.Canvas(output_pdf, pagesize=(adjusted_page_width, adjusted_page_height))
    c.setPageCompression(1)  # Use page compression

    # Define the size of A6 at the new DPI
    a6_width = adjusted_page_width / 2
    a6_height = adjusted_page_height / 2

    # Open the images
    image1 = Image.open(input_image1)
    image2 = Image.open(input_image2)

    # Resize images using high-quality resampling
    image1 = image1.resize((int(a6_width), int(a6_height)), Image.LANCZOS)
    image2 = image2.resize((int(a6_width), int(a6_height)), Image.LANCZOS)

    # Create A4 page with image1 in A6 segments
    for i in range(2):
        for j in range(2):
            c.drawInlineImage(image1, x=j * a6_width, y=adjusted_page_height - (i + 1) * a6_height, width=a6_width,
                              height=a6_height)

    # Add another page for image2
    c.showPage()

    # Create A4 page with image2 in A6 segments
    for i in range(2):
        for j in range(2):
            c.drawInlineImage(image2, x=j * a6_width, y=adjusted_page_height - (i + 1) * a6_height, width=a6_width,
                              height=a6_height)

    c.save()


# Specify the input file names and the output PDF name
create_pdf('page_1.png', 'page_2.png', 'output.pdf')
