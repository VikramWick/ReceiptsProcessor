import pytesseract
from PIL import Image
import re
from datetime import datetime
from PyPDF2 import PdfReader
import io

def extract_text_from_image(image_stream) -> str:
    """Extracts raw text from an image using Tesseract OCR."""
    image = Image.open(image_stream)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_stream) -> str:
    """Extracts text from a PDF file."""
    pdf = PdfReader(pdf_stream)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(txt_stream) -> str:
    """Reads text from a text file stream."""
    return txt_stream.read().decode("utf-8")

def parse_receipt_data(text: str) -> dict:
    """Parses vendor, date, and total from raw receipt text using regex."""
    data = {"vendor": None, "date": None, "total": None}

    # Vendor: Look for a common name or the first non-empty line.
    lines = [line for line in text.split('\n') if line.strip()]
    if lines:
        data["vendor"] = lines[0].strip()

    # Date: Look for DD/MM/YYYY, MM-DD-YYYY, YYYY-MM-DD etc.
    date_match = re.search(r'(\d{1,4}[-/]\d{1,2}[-/]\d{1,4})', text)
    if date_match:
        try:
            date_str = date_match.group(1)
            # Normalize separators and try different formats
            normalized_date = date_str.replace('-', '/')
            if len(normalized_date.split('/')[2]) == 4: # DD/MM/YYYY
                data["date"] = datetime.strptime(normalized_date, "%d/%m/%Y")
            elif len(normalized_date.split('/')[0]) == 4: # YYYY/MM/DD
                 data["date"] = datetime.strptime(normalized_date, "%Y/%m/%d")
            else: # MM/DD/YY
                 data["date"] = datetime.strptime(normalized_date, "%m/%d/%y")
        except (ValueError, IndexError):
            pass

    # Total: Look for lines with "Total", "Amount", etc. and find the largest number.
    potential_totals = re.findall(r'(?i)(?:total|amount|balance|due)[\s:]*.*?(\d+\.\d{2})', text)
    if potential_totals:
        data["total"] = max([float(t) for t in potential_totals])
    else: # Fallback: find the largest monetary value in the document
        all_monetary_values = re.findall(r'\d+\.\d{2}', text)
        if all_monetary_values:
            data["total"] = max([float(v) for v in all_monetary_values])

    return data