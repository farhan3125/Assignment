## Importing all the necessary packages
import pandas as pd
from PIL import Image
import numpy as np
#import sqlite3
#from io import BytesIO
#from flask import Flask, request, send_file
import matplotlib.pyplot as plt
from flask import Flask, request, send_file, jsonify
import sqlite3
from io import BytesIO


# Reading the CSV file. Have named the filename of csv as Challenge.scv
df = pd.read_csv('Challenge.csv')

# Extract pixel data from dataframe
image_data = df.drop(columns=['depth']).to_numpy()

# Reshaping the data to its original dimensions
original_height, original_width = image_data.shape[0], 200
image_data = image_data.reshape((original_height, original_width))

# Converting the same to Image
image = Image.fromarray(np.uint8(image_data), 'L')

# Resizing Image. This was instrcuted in the shared use case
resized_image = image.resize((150, original_height), Image.Resampling.LANCZOS)
resized_image.save('resized_image.png')


# Connecting to to the database
## Here , I am intensinally reconnecting the DB for every request
conn = sqlite3.connect('images.db')
cursor = conn.cursor()

# Creating table. Keeping it simple. Without any Datetime column for tracking.
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY,
    depth INTEGER,
    image BLOB
)
''')

# Converting the image to binary
image_blob = BytesIO()
resized_image.save(image_blob, format='PNG')
image_blob = image_blob.getvalue()

# Inserting image into database.
depth = 0  # Assuming depth value for this example
cursor.execute('INSERT INTO images (depth, image) VALUES (?, ?)', (depth, image_blob))
conn.commit()


app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('images.db')
    conn.row_factory = sqlite3.Row
    return conn

def apply_custom_color_map(image_data, cmap='viridis'):
    img = Image.open(BytesIO(image_data))
    img = np.array(img)

    plt.imshow(img, cmap=cmap)
    plt.axis('off')

    output = BytesIO()
    plt.savefig(output, format='PNG', bbox_inches='tight', pad_inches=0)
    output.seek(0)

    return output

@app.route('/')
def home():
    return "The second challenge is up and running."

@app.route('/get_image', methods=['GET'])
def get_image():
    depth_min = request.args.get('depth_min')
    depth_max = request.args.get('depth_max')


    ## Have tried to cover as many exceptions as I can with limited time.
    if depth_min is None or depth_max is None:
        return jsonify({"error": "provide both depth_min and depth_max parameters"}), 400

    try:
        depth_min = int(depth_min)
        depth_max = int(depth_max)
    except ValueError:
        return jsonify({"error": "depth_min and depth_max must be integers"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT image FROM images WHERE depth BETWEEN ? AND ?', (depth_min, depth_max))
    image_data = cursor.fetchone()
    conn.close()

    if image_data is None:
        return jsonify({"error": "No image found for the given depth range"}), 404

    colored_image = apply_custom_color_map(image_data['image'], cmap='plasma')

    return send_file(colored_image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
