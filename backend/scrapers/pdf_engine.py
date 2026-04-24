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
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        
        if not text.strip():
            return "Warning: Could not extract any readable text from this PDF. Please ensure it is not an image-only scan."
            
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return f"Error reading syllabus PDF: {str(e)}"
