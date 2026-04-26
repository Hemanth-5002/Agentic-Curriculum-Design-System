from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import io

def generate_curriculum_pdf(data: dict) -> bytes:
    """
    Generate a professional PDF for the curriculum.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#00f0ff"),
        spaceAfter=20
    )
    
    story = []
    
    # University Name
    uni_style = ParagraphStyle(
        'UniStyle',
        parent=styles['Normal'],
        fontSize=20,
        textColor=colors.HexColor("#0a0f1c"),  # Dark blue/black for visibility
        spaceAfter=5
    )
    story.append(Paragraph(data.get('university_name', 'University Curriculum').upper(), uni_style))
    
    # Domain Title
    story.append(Paragraph(f"{data['domain']} Blueprint", title_style))
    story.append(Spacer(1, 10))
    
    # Key Highlights (The 4 points requested)
    story.append(Paragraph("<b>Key Curriculum Highlights:</b>", styles['Heading3']))
    highlights = [
        "• <b>Industry Alignment:</b> Mapped to 2024 real-time job market requirements.",
        "• <b>Research Driven:</b> Includes latest findings from ArXiv academic repositories.",
        "• <b>Specialization Focus:</b> Designed for modern career paths in " + data['domain'] + ".",
        "• <b>Practical Readiness:</b> Balanced credit distribution for hands-on learning."
    ]
    for point in highlights:
        story.append(Paragraph(point, styles['Normal']))
    
    story.append(Spacer(1, 20))
    
    # Gap Analysis
    gap_analysis = data.get('gap_analysis', '')
    if gap_analysis and gap_analysis.strip() and "Full modern implementation required" not in gap_analysis:
        story.append(Paragraph("<b>Gap Analysis (What needs to be implemented):</b>", styles['Heading3']))
        story.append(Paragraph(gap_analysis, styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Modules (Point-wise)
    story.append(Paragraph("<b>Proposed Curriculum Modules:</b>", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    for i, mod in enumerate(data['modules']):
        # Point-wise Title
        story.append(Paragraph(f"<b>{i+1}. {mod['title']} ({mod['credit_hours']} Credits)</b>", styles['Normal']))
        # Description (maintains line breaks if present)
        story.append(Paragraph(f"{mod['description']}", styles['Normal']))
        story.append(Spacer(1, 15))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
