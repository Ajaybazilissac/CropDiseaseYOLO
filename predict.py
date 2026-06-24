from ultralytics import YOLO

model = YOLO("runs/detect/train-9/weights/best.pt")

results = model.predict(
    source="test_images",
    conf=0.25,
    save=True
)

print("Prediction completed")