from ultralytics import YOLO
model = YOLO("yolo11n.pt")
model.train(
    data="dataset/dataset.yaml", 
    epochs=1, 
    imgsz=640, 
    batch=8
    )