from pypdf import PdfReader
import io

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from a PDF file provided as bytes.
    """
    try:
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return "Error reading syllabus PDF."
