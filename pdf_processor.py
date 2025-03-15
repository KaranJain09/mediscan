import io
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\skintern\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'


def extract_text_from_pdf(file) -> str:
    """
    Extract text from a PDF file robustly.
    
    Uses PyMuPDF to extract embedded text; if the extracted text from a page 
    is very short (suggesting a scanned page or poor quality text), it falls back 
    to OCR using Tesseract.
    """
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    all_text = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        # First try to extract text directly
        text = page.get_text("text")
        # If text is very short, assume OCR might be needed
        if len(text.strip()) < 50:
            try:
                # Render page as an image at a higher resolution (300 dpi)
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                # Use Tesseract to extract text from the image
                text = pytesseract.image_to_string(img)
            except Exception as e:
                print(f"OCR failed on page {page_num}: {e}")
        all_text.append(text)
    
    pdf_document.close()
    return "\n".join(all_text)

