import pdfplumber

def extract_text_from_file(uploaded_file):
    """Accepts a file-like object (Streamlit uploaded file) and returns extracted text."""
    # Try to detect by file name / type
    name = uploaded_file.name.lower()

    if name.endswith('.txt'):
        # Read plain text file
        text = uploaded_file.getvalue().decode('utf-8', errors='ignore')
        return text

    elif name.endswith('.pdf'):
        # Use pdfplumber to extract text
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                pages = [p.extract_text() or '' for p in pdf.pages]
            return '\n'.join(pages)
        except Exception as e:
            return f"[Error extracting PDF text: {e}]"

    else:
        # Fallback — try to read as UTF-8 text
        try:
            return uploaded_file.getvalue().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"[Error reading file: {e}]"
