import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from ultralytics import YOLO

app = Flask(__name__, static_folder="static")
model = YOLO("runs/detect/train/weights/best.pt")  # Load trained model

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = "uploaded.jpg"
    file.save(filename)

    # Load the uploaded image
    img = cv2.imread(filename)
    if img is None:
        return jsonify({"error": "Image upload failed"}), 500  # Handle if the image fails to load

    # Run detection
    results = model(img)

    # Define font & colors
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    color = (0, 255, 0)  # Green for bounding boxes

    # Process each detection result
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            confidence = box.conf[0]  # Get confidence score
            label = model.names[int(box.cls[0])]  # Get label (class name)

            # Draw bounding box first
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

            # Convert confidence score to percentage
            text = f"{label}: {confidence * 100:.2f}%"  # Example: "Tile Roof: 85.32%"

            # Calculate text size and position
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_x, text_y = x1, y1 - 10 if y1 - 10 > 10 else y1 + 20  # Position text

            # Draw black background for text
            cv2.rectangle(img, 
                          (text_x, text_y - text_size[1] - 5), 
                          (text_x + text_size[0] + 5, text_y + 5), 
                          (0, 0, 0), -1)  

            # Draw label with confidence
            cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

    # Ensure static directory exists
    if not os.path.exists("static"):
        os.makedirs("static")

    output_filename = os.path.join("static", "output.jpg")
    success = cv2.imwrite(output_filename, img)  # Save processed image

    if not success:
        return jsonify({"error": "Failed to save output image"}), 500

    return jsonify({"output": "/static/output.jpg"})  # Return path to processed image

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
