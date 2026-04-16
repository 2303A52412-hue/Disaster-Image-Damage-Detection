from flask import Flask, render_template, request
import os
from model import detect_damage

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    # Call damage detection
    output_path = detect_damage(img_path)

    return render_template('index.html', result_image=output_path)

if __name__ == '__main__':
    app.run(debug=True)