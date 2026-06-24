import streamlit as st


from ultralytics import YOLO
from PIL import Image
import tempfile
import plotly.express as px

from disease_info import disease_data
from report_generator import generate_report

# Load YOLO model
model = YOLO("best.pt")

# Page configuration
st.set_page_config(
    page_title="Crop Disease Detection",
    page_icon="🌱",
    layout="wide"
)

# Sidebar
st.sidebar.title("🌱 Project Information")

st.sidebar.markdown("""
### Crop Disease Detection

**Model:** YOLOv11

**Classes:** 9

**Training Images:** 2832

**Framework:** PyTorch

**Frontend:** Streamlit

**Developer:** Ajay Bazil Issac
""")

st.sidebar.markdown("---")

st.sidebar.metric("Classes", "9")
st.sidebar.metric("Images", "2832")
st.sidebar.metric("Model", "YOLOv11")

# Main Page
st.title("🌱 AI Crop Disease Detection System")

st.caption(
    "Deep Learning based Tomato Leaf Disease Detection using YOLOv11"
)

st.write(
    "Upload a tomato leaf image and the AI model will detect the disease and suggest treatment recommendations."
)

# File Upload
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        width=400
    )

    if st.button("Detect Disease"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as temp_file:

            image.save(temp_file.name)

            results = model.predict(
                source=temp_file.name,
                conf=0.25
            )

        result = results[0]

        # Show detected image
        annotated_image = result.plot()

        st.subheader("Detection Result")

        st.image(
            annotated_image,
            caption="Detected Diseases",
            width=400
        )

        st.subheader("Prediction Results")

        if len(result.boxes) == 0:

            st.warning("No disease detected.")

        else:

            detections = []
            disease_counts = {}

            for box in result.boxes:

                class_id = int(box.cls[0])

                confidence = float(box.conf[0])

                disease_name = model.names[class_id]
                
                if disease_name in disease_counts:
                    disease_counts[disease_name] += 1
                else:
                    disease_counts[disease_name] = 1

                info = disease_data.get(disease_name)

                # Save for PDF
                if info:

                    detections.append({
                        "name": disease_name,
                        "confidence": confidence,
                        "description": info["description"],
                        "treatment": info["treatment"]
                    })

                st.success(
                    f"🦠 Detected Disease: {disease_name}"
                )

                st.write(
                    f"**Confidence:** {confidence:.2%}"
                )

                st.progress(float(confidence))

                if info:

                    st.write(
                        f"**Description:** {info['description']}"
                    )

                    st.info(
                        f"Treatment Recommendation: {info['treatment']}"
                    )

                st.markdown("---")

            # Generate PDF
            pdf_file = generate_report(detections)

            with open(pdf_file, "rb") as file:

                st.download_button(
                label="📄 Download Report",
                data=file,
                file_name="crop_disease_report.pdf",
                mime="application/pdf"
                 )

        # Disease Distribution Chart
            st.subheader("📊 Disease Distribution")

            fig = px.pie(
                 values=list(disease_counts.values()),
                 names=list(disease_counts.keys()),
                 title="Detected Diseases"
                )

            st.plotly_chart(fig, use_container_width=True)