import PyPDF2
import sys
import fitz
import difflib
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.

    Args:
    pdf_file (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF.
    """
    doc = fitz.open(pdf_file)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def compare_texts(text1, text2):
    """
    Compares two texts and generates an HTML diff.

    Args:
    text1 (str): The first text to compare.
    text2 (str): The second text to compare.

    Returns:
    str: HTML representation of the differences between the two texts.
    """
    d = difflib.HtmlDiff()
    diff_html = d.make_file(text1.splitlines(), text2.splitlines())
    return diff_html

def generate_comparison_pdf(pdf_file1, pdf_file2, output_pdf):
    """
    Generates a PDF file that contains a side-by-side comparison of two PDF files.

    Args:
    pdf_file1 (str): The path to the first PDF file.
    pdf_file2 (str): The path to the second PDF file.
    output_pdf (str): The path where the comparison PDF will be saved.
    """
    text1 = extract_text_from_pdf(pdf_file1)
    text2 = extract_text_from_pdf(pdf_file2)

    # Create a new PDF to write the comparison
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    margin = 1 * inch

    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    
    # Start from the top of the page
    y_position = height - margin  

    # Loop through the diff and add text with color coding
    for line in diff:
        if line.startswith('-'):
            c.setFillColor(colors.red)
        elif line.startswith('+'):
            c.setFillColor(colors.green)
        else:
            c.setFillColor(colors.black)

        # Write the line to the PDF, adjust for side-by-side layout
        # Ignore the first two characters (-/+/ )
        c.drawString(margin, y_position, line[2:])  

        # Move down for the next line
        y_position -= 12
        # Check if we need a new page
        if y_position < margin:
            c.showPage()
            y_position = height - margin

    c.save()

def count_pages_and_lines(pdf_path):
    """
    Counts the number of pages and non-empty lines on the last page of a PDF.

    Args:
    pdf_path (str): The path to the PDF file.

    Returns:
    tuple: A tuple containing the number of pages and the count of non-empty lines on the last page.
    """

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        num_pages = len(pdf_reader.pages)
        
        print(f"Total number of pages: {num_pages}")
        
        # Count lines on each page
        # for page_num in range(num_pages):
        #     page = pdf_reader.pages[page_num]
        #     text = page.extract_text()
            
        #     # Count the lines
        #     lines = text.split('\n')
        #     line_count = len([line for line in lines if line.strip()])  # Count non-empty lines
            
        #     print(f"Page {page_num + 1}: {line_count} lines")
        
        last_page = num_pages - 1
        page = pdf_reader.pages[last_page]
        text = page.extract_text()
        lines = text.split('\n')
        line_count = len([line for line in lines if line.strip()])
        return num_pages, line_count

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_pages_and_lines.py path/to/your/resume.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    print(count_pages_and_lines(pdf_path))