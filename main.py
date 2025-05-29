from flask import Flask, request, jsonify
from model_predictor import FacePredictor
import os

app = Flask(__name__)

# Konfigurasi Classes
CLASSES_CONFIG = {
    "0": "Nesha",
    "1": "Syauqi",
}  # Bisa juga path ke file JSON

# Initialize predictor
predictor = FacePredictor(
    model_path='arcface_model.h5',
    classes_config=CLASSES_CONFIG  # atau 'path/to/classes.json'
)

@app.route('/update_classes', methods=['POST'])
def update_classes():
    """Endpoint untuk update class mapping secara dinamis"""
    new_classes = request.json
    if not isinstance(new_classes, dict):
        return jsonify({"error": "Invalid format"}), 400
    
    predictor.classes = new_classes
    return jsonify({"message": "Classes updated", "new_classes": new_classes})

@app.route('/embed', methods=['POST'])
def handle_embed():
    print("Method:", request.method)
    print("Headers:", dict(request.headers))
    print("Args:", request.args)  # Query parameters
    print("Form:", request.files)  # Form data
    print("Form:", request.form)  # Form data
    print("JSON:", request.get_json(silent=True))
    if 'image' not in request.files:
        return jsonify({"error": "No image data provided"}), 400
    
    x = int(request.form.get('x'))
    y = int(request.form.get('y'))
    
    image_file = request.files['image']
    result = predictor.embed(image_file, face_pos=(x, y))
    
    return jsonify(result)

@app.route('/something')
def handle_something():
    return "something"


@app.route('/', methods=['POST'])
def handle_prediction():
    if 'image' not in request.files:
        return jsonify({"error": "No image data provided"}), 400
    
    image_file = request.files['image']
    result = predictor.predict(image_file)
    
    return jsonify(result)

@app.route('/', methods=['GET'])
def handle_root():
    return jsonify({"message":"Hellow"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_ENV') == 'development')
