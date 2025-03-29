from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Using the smallest model for training

# Train model on your dataset
model.train(data="C:/Users/koush/OneDrive/Desktop/Orthophotos Detection/Orthophotos-4/data.yaml", 
            epochs=50, imgsz=640)

# Model weights will be saved in runs/detect/train/weights/best.pt
