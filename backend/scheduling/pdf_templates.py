from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

def generate_simple_call_sheet(call_sheet):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, height - inch, f"Call Sheet: {call_sheet.production.title}")
    p.setFont("Helvetica", 12)
    p.drawString(inch, height - 1.25 * inch, f"Date: {call_sheet.date}")

    y_position = height - 2.5 * inch
    p.setFont("Helvetica-Bold", 14)
    p.drawString(inch, y_position, "Locations")
    y_position -= 0.25 * inch
    p.setFont("Helvetica", 10)
    if call_sheet.locations:
        for location in call_sheet.locations:
            p.drawString(1.2 * inch, y_position, f"- {location.get('name', 'N/A')}: {location.get('address', 'N/A')}")
            y_position -= 0.25 * inch
    else:
        p.drawString(1.2 * inch, y_position, "No locations specified.")
        y_position -= 0.25 * inch

    y_position -= 0.5 * inch
    p.setFont("Helvetica-Bold", 14)
    p.drawString(inch, y_position, "Scenes to be Shot")
    y_position -= 0.25 * inch
    p.setFont("Helvetica", 10)
    scenes_str = ", ".join(map(str, call_sheet.scenes)) if call_sheet.scenes else "No scenes specified."
    p.drawString(1.2 * inch, y_position, scenes_str)

    y_position -= 0.5 * inch
    p.setFont("Helvetica-Bold", 14)
    p.drawString(inch, y_position, "Crew Assignments")
    y_position -= 0.25 * inch
    p.setFont("Helvetica", 10)
    if call_sheet.crew_assignments:
        for user_id, details in call_sheet.crew_assignments.items():
            p.drawString(1.2 * inch, y_position, f"- User ID {user_id}: Call at {details.get('call_time', 'N/A')} as {details.get('role', 'N/A')}")
            y_position -= 0.25 * inch
    else:
        p.drawString(1.2 * inch, y_position, "No crew assignments specified.")
        y_position -= 0.25 * inch

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf