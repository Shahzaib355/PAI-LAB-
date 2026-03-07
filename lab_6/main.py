"""
Lab 6 - Animal Herd Detection Flask App
Programming for Artificial Intelligence
Superior University Lahore
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import numpy as np
import base64
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

os.makedirs('uploads', exist_ok=True)
os.makedirs('results', exist_ok=True)

# ── Animal Detection using color + contour analysis ──
# Since YOLO requires internet to download weights, we use
# OpenCV's built-in Haar Cascades + contour-based detection

ANIMAL_COLORS = {
    'brown':  ([10, 50, 50],  [30, 255, 200]),   # Brown animals (cows, horses)
    'black':  ([0, 0, 0],     [180, 60, 60]),     # Black animals
    'white':  ([0, 0, 200],   [180, 30, 255]),    # White animals (sheep)
    'gray':   ([0, 0, 80],    [180, 30, 180]),    # Gray animals
}

def detect_animals(image_path):
    """
    Detect animals using color segmentation + contour analysis.
    Returns annotated image and detection stats.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None, {}

    original = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = img.shape[:2]

    # ── Step 1: Background removal using GrabCut (simplified) ──
    # Convert to grayscale and apply thresholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # ── Step 2: Find large blobs (potential animals) ──
    # Use edge detection + morphology to find animal shapes
    edges = cv2.Canny(blurred, 20, 80)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    dilated = cv2.dilate(edges, kernel, iterations=3)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by area — animals should be reasonably large
    min_area = (h * w) * 0.005   # at least 0.5% of image
    max_area = (h * w) * 0.6     # at most 60% of image
    animal_contours = [c for c in contours if min_area < cv2.contourArea(c) < max_area]

    # ── Step 3: Draw detections ──
    result = original.copy()
    detections = []

    for i, cnt in enumerate(animal_contours):
        x, y, bw, bh = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        cx = x + bw // 2
        cy = y + bh // 2

        # Determine dominant color in this region
        roi = hsv[y:y+bh, x:x+bw]
        mean_hue = np.mean(roi[:,:,0])
        mean_sat = np.mean(roi[:,:,1])
        mean_val = np.mean(roi[:,:,2])

        # Guess animal type from color
        if mean_val < 60:
            animal_type = "Dark Animal"
            box_color = (50, 50, 50)
        elif mean_sat < 40:
            animal_type = "Light Animal (Sheep?)"
            box_color = (200, 200, 200)
        elif 10 < mean_hue < 25:
            animal_type = "Brown Animal (Cow/Horse?)"
            box_color = (30, 100, 180)
        elif 35 < mean_hue < 85:
            animal_type = "Green-region Animal"
            box_color = (0, 180, 0)
        else:
            animal_type = "Animal"
            box_color = (0, 200, 255)

        # Draw bounding box
        cv2.rectangle(result, (x, y), (x+bw, y+bh), box_color, 3)

        # Draw contour
        cv2.drawContours(result, [cnt], -1, box_color, 2)

        # Label
        label = f"#{i+1} {animal_type}"
        (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
        cv2.rectangle(result, (x, y - lh - 10), (x + lw + 8, y), box_color, -1)
        cv2.putText(result, label, (x + 4, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        # Center dot
        cv2.circle(result, (cx, cy), 5, (0, 255, 255), -1)

        detections.append({
            'id': i + 1,
            'type': animal_type,
            'bbox': [int(x), int(y), int(bw), int(bh)],
            'area': int(area),
            'center': [int(cx), int(cy)]
        })

    # ── Herd classification ──
    count = len(detections)
    if count == 0:
        herd_status = "No Animals Detected"
        alert_level = "none"
    elif count < 3:
        herd_status = "Small Group"
        alert_level = "low"
    elif count < 8:
        herd_status = "Medium Herd"
        alert_level = "medium"
    else:
        herd_status = "Large Herd — ALERT!"
        alert_level = "high"

    # ── Overlay summary on image ──
    overlay = result.copy()
    cv2.rectangle(overlay, (0, 0), (w, 70), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, result, 0.4, 0, result)

    summary = f"HERD DETECTION | Count: {count} | Status: {herd_status}"
    cv2.putText(result, summary, (15, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 200), 2)

    # Save result
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_path = f"results/result_{timestamp}.jpg"
    cv2.imwrite(result_path, result)

    stats = {
        'count': count,
        'herd_status': herd_status,
        'alert_level': alert_level,
        'detections': detections,
        'result_image': result_path,
        'timestamp': timestamp,
        'image_size': f"{w}x{h}"
    }

    return result, stats


def image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save uploaded file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"upload_{timestamp}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Run detection
    result_img, stats = detect_animals(filepath)

    if result_img is None:
        return jsonify({'error': 'Could not process image'}), 500

    # Convert result image to base64
    result_b64 = image_to_base64(result_img)

    return jsonify({
        'success': True,
        'result_image': f"data:image/jpeg;base64,{result_b64}",
        'stats': stats
    })


@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory('results', filename)


if __name__ == '__main__':
    print("🐄 Animal Herd Detection App Starting...")
    print("   Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
