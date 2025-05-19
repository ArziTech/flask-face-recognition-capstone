from flask import Blueprint, request, jsonify
from ..models import User
from ..model_predictor import FacePredictor
import os

main = Blueprint('main', __name__)

# Konfigurasi Classes
CLASSES_CONFIG = {
    "0": "Nesha",
    "1": "Syauqi",
}  # Bisa juga path ke file JSON

model_path = os.path.join('app', 'static', 'models', 'arcface_model.h5')

# Initialize predictor
predictor = FacePredictor(
    model_path=model_path,
    classes_config=CLASSES_CONFIG  # atau 'path/to/classes.json'
)

@main.route('/')
def index():
    users = User.query.all()
    # bagaimana cara mengembalikan user sebagai response, karena saya mendapatkan error object not serializable
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)

@main.route('/update_classes', methods=['POST'])
def update_classes():
    """Endpoint untuk update class mapping secara dinamis"""
    new_classes = request.json
    if not isinstance(new_classes, dict):
        return jsonify({"error": "Invalid format"}), 400
    
    predictor.classes = new_classes
    return jsonify({"message": "Classes updated", "new_classes": new_classes})

@main.route('/embed', methods=['POST'])
def handle_embed():
    if 'image' not in request.files:
        return jsonify({"error": "No image data provided"}), 400
    
    image_file = request.files['image']
    result = predictor.embed(image_file)
    
    return jsonify(result)

@main.route('/', methods=['POST'])
def handle_prediction():
    if 'image' not in request.files:
        return jsonify({"error": "No image data provided"}), 400
    
    image_file = request.files['image']
    result = predictor.predict(image_file)
    
    return jsonify(result)