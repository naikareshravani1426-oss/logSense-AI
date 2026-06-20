import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf(result: dict, raw_log: str, log_id: str):
    path = os.path.join(REPORTS_DIR, f"logsense_{log_id}.pdf")
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("LogSense Diagnostic Report", styles['Title']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Domain: " + result.get('domain', ''), styles['Heading2']))
    story.append(Paragraph("Severity: " + result.get('severity', ''), styles['Heading2']))
    story.append(Paragraph("Confidence: " + str(result.get('confidence', '')), styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Diagnosis", styles['Heading3']))
    story.append(Paragraph(result.get('diagnosis', ''), styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Cause", styles['Heading3']))
    story.append(Paragraph(result.get('cause', ''), styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Fix Steps", styles['Heading3']))
    for index, step in enumerate(result.get('fix_steps', []), 1):
        story.append(Paragraph(f"{index}. {step}", styles['Normal']))

    doc.build(story)
    return path
