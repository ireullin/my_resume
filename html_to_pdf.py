import pdfkit
import sys
import os

def convert_html_to_pdf(html_path, pdf_path):
    """Converts an HTML file to a PDF file using pdfkit."""
    try:
        if not os.path.exists(html_path):
            print(f"Error: Input file not found at '{html_path}'")
            return

        print(f"Reading HTML from: {html_path}")
        
        # Options to preserve styling
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'enable-local-file-access': None
        }

        pdfkit.from_file(html_path, pdf_path, options=options)
        
        print(f"Successfully created PDF: {pdf_path}")

    except Exception as e:
        print(f"An error occurred during PDF conversion: {e}")
        print("This might be because wkhtmltopdf is not installed or not in your PATH.")
        print("Please install it from https://wkhtmltopdf.org/downloads.html")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python html_to_pdf.py <input_html_file> <output_pdf_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_html_to_pdf(input_file, output_file)