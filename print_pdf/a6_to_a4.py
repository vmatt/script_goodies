import fitz  # PyMuPDF

def resize_and_place_pdf(input_path, output_path):
    # Open the input PDF
    src_doc = fitz.open(input_path)
    src_page = src_doc[0]

    # Create a new A4 PDF
    dst_doc = fitz.open()
    dst_page = dst_doc.new_page(width=595, height=842)  # A4 size in points

    # Render the source page to a pixmap
    zoom = 2  # Increase this for higher quality
    mat = fitz.Matrix(zoom, zoom)
    pix = src_page.get_pixmap(matrix=mat)

    # Get the dimensions of the rendered content
    src_width = pix.width / zoom
    src_height = pix.height / zoom

    # Calculate the scaling factor to fit the source page into a quarter of A4
    scale_factor = min(dst_page.rect.width / (2 * src_width),
                       dst_page.rect.height / (2 * src_height))

    # Calculate the scaled dimensions
    scaled_width = src_width * scale_factor
    scaled_height = src_height * scale_factor

    # Define the positions for the 4 placements
    positions = [
        (0, 0),                             # Top-left
        # (dst_page.rect.width / 2, 0),       # Top-right
        # (0, dst_page.rect.height / 2),      # Bottom-left
        # (dst_page.rect.width / 2, dst_page.rect.height / 2)  # Bottom-right
    ]

    # Place the source page 4 times on the destination page
    for x, y in positions:
        dst_page.insert_image(
            fitz.Rect(x, y, x + scaled_width, y + scaled_height),
            pixmap=pix
        )

    # Save the result
    dst_doc.save(output_path, garbage=4, deflate=True, clean=True)
    dst_doc.close()
    src_doc.close()

# Usage
input_file = "cimke.pdf"
output_file = "output_A4_with_4xcimke.pdf"

resize_and_place_pdf(input_file, output_file)
print(f"Created {output_file}")
