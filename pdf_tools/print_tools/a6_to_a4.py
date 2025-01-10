import fitz  # PyMuPDF

def resize_and_place_pdf(input_path, output_path):
    with fitz.open(input_path) as src_doc, fitz.open() as dst_doc:
        src_page = src_doc[0]
        dst_page = dst_doc.new_page(width=595, height=842)  # A4 size in points

        # Render the source page to a pixmap
        zoom = 2  # Increase this for higher quality
        pix = src_page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))

        # Get the dimensions of the rendered content
        src_width = pix.width / zoom
        src_height = pix.height / zoom

        # Calculate the scaling factor to fit the source page into a quarter of A4
        scale_factor = min(dst_page.rect.width / (2 * src_width),
                           dst_page.rect.height / (2 * src_height))

        # Calculate the scaled dimensions
        scaled_width = src_width * scale_factor
        scaled_height = src_height * scale_factor

        # Place the source page on the top-left of the destination page
        dst_page.insert_image(
            fitz.Rect(0, 50, scaled_width, scaled_height),
            pixmap=pix
        )

        dst_doc.save(output_path, garbage=4, deflate=True, clean=True)

# Usage
input_file = "cimke.pdf"
output_file = "output_A4_with_cimke.pdf"

resize_and_place_pdf(input_path=input_file, output_path=output_file)
print(f"Created {output_file}")
