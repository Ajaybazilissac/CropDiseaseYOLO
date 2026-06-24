from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


def generate_report(detections, filename="crop_disease_report.pdf"):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "Crop Disease Detection Report",
        styles["Title"]
    )

    content.append(title)

    content.append(Spacer(1, 12))

    date_text = Paragraph(
        f"Generated On: {datetime.now()}",
        styles["Normal"]
    )

    content.append(date_text)

    content.append(Spacer(1, 20))

    for disease in detections:

        content.append(
            Paragraph(
                f"<b>Disease:</b> {disease['name']}",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Confidence:</b> {disease['confidence']:.2%}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Description:</b> {disease['description']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Treatment:</b> {disease['treatment']}",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 15)
        )

    doc.build(content)

    return filename