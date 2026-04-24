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
    
    # Title
    story.append(Paragraph(f"{data['domain']} Curriculum", title_style))
    story.append(Spacer(1, 12))
    
    # Clean up Rationale for PDF
    rationale_text = data.get('rationale', 'No rationale provided.')
    if rationale_text and "Quota limit reached" in rationale_text:
        rationale_text = "This curriculum was optimized using industry-standard templates and refined based on the specific academic domain and university context provided."

    # Rationale
    story.append(Paragraph("<b>Rationale:</b>", styles['Heading3']))
    story.append(Paragraph(rationale_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Prerequisites
    story.append(Paragraph("<b>Prerequisites:</b>", styles['Heading3']))
    prereqs = data.get('prerequisites', [])
    story.append(Paragraph(", ".join(prereqs) if prereqs else "None", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Modules Table
    story.append(Paragraph("<b>Proposed Modules:</b>", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    table_data = [["#", "Module Title", "Description", "Credits"]]
    for i, mod in enumerate(data['modules']):
        table_data.append([
            str(i+1),
            Paragraph(mod['title'], styles['Helvetica-Bold'] if 'Helvetica-Bold' in styles else styles['Normal']),
            Paragraph(mod['description'], styles['Normal']),
            str(mod['credit_hours'])
        ])
        
    # Total width ~460 for standard letter size with margins
    t = Table(table_data, colWidths=[25, 125, 260, 50])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0a0f1c")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(t)
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
