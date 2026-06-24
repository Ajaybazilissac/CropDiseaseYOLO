from ultralytics import YOLO

def main():
    model = YOLO("yolo11s.pt")

    model.train(
        data="dataset/data.yaml",
        epochs=50,
        imgsz=640,
        batch=4,
        workers=0,
        device=0
    )

if __name__ == "__main__":
    main()