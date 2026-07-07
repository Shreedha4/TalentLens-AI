import re
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts and normalizes text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): The absolute path to the PDF file.
        
    Returns:
        str: The extracted, cleaned text from the PDF.
    """
    text = ""
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        # Iterate through pages and extract text
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
        
        doc.close()
    except Exception as e:
        # Log or return an error context if the file fails to parse
        raise RuntimeError(f"Failed to parse PDF file at {pdf_path}: {str(e)}")
        
    return clean_text(text)

def clean_text(text: str) -> str:
    """
    Cleans raw text by normalizing whitespaces, removing control characters,
    and trimming margins.
    
    Args:
        text (str): Raw string content.
        
    Returns:
        str: Cleaned, normalized string.
    """
    # Replace multiple spaces/tabs/newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing spaces
    return text.strip()
