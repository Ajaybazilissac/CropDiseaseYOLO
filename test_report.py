from report_generator import generate_report

sample_data = [
    {
        "name": "Tomato Septoria leaf spot",
        "confidence": 0.91,
        "description": "A fungal disease causing leaf spots.",
        "treatment": "Apply fungicide."
    }
]

generate_report(sample_data)

print("PDF Generated Successfully")