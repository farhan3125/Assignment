## Importing all the necessasry packages
from flask import Flask, request, jsonify
import os
import uuid
import cv2
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  ## Keeping the folder nmae
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

## For checking if the application is runing well
@app.route('/')
def home():
    return "App is running well"

## To upload the file
## kept circle_coin.jpg for all the loaded file. Could have handled it better but with limited time and just the solution to work well.
## Also, handled a few scnario if the file is not uploaded etc.
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    #filename = str(uuid.uuid4()) + '.jpg'
    filename = "circle_coin" + '.jpg'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return jsonify({'filename': filename}), 200


## In actual while making the request we will always give the file name as circle_coin.jpg.
## Jsut to keep the solution simple
@app.route('/circles/<filename>', methods=['GET'])
def get_circles(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Processing file: {file_path}")  # Debugging log
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15),
                               0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=10,
                               maxRadius=100)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int").tolist()  # Convert to list of standard integers
        result = []
        for i, (x, y, r) in enumerate(circles):
            # Here , Drawing the the circle
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 4)
            # Here , Drawing  the bounding box
            cv2.rectangle(image, (int(x - r), int(y - r)), (int(x + r), int(y + r)), (0, 128, 255), 2)
            # Giving unique reference number, centroid, radius
            cv2.putText(image, f'ID: {i}', (int(x - r), int(y - r) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(image, f'Centroid: ({int(x)}, {int(y)})', (int(x - r), int(y - r) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(image, f'Radius: {int(r)}', (int(x - r), int(y - r) + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 0, 255), 2)
            result.append({
                'id': i,
                'bounding_box': [int(x - r), int(y - r), int(x + r), int(y + r)],
                'centroid': (int(x), int(y)),
                'radius': int(r)
            })
        # Saving the annotated image. It will always be saved with the same name to keep the soultion simple
        output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"annotated_{filename}")
        cv2.imwrite(output_file_path, image)
        return jsonify({'circles': result, 'annotated_image': output_file_path}), 200
    else:
        return jsonify({'error': 'No circles found'}), 400


if __name__ == '__main__':
    app.run(debug=True)
