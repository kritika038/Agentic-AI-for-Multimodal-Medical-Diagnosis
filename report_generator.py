

def generate_report(pneumonia, diabetes, confidence):

    report = ""

    if pneumonia:
        report += "Chest X-ray analysis indicates signs of lung infection consistent with pneumonia.\n"
        report += f"Model confidence: {confidence:.2f}%\n"
    else:
        report += "No pneumonia indicators detected in the X-ray.\n"

    if diabetes:
        report += "Patient clinical parameters indicate elevated diabetes risk.\n"
    else:
        report += "Diabetes risk appears within normal range.\n"

    report += "\nThis AI system provides preliminary medical screening only."
    report += "\nPlease consult a qualified doctor for confirmation."

    return report