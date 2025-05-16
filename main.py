from flask import Flask, request, jsonify
import cv2
import numpy as np
from keras.models import load_model
import base64
import io
from PIL import Image

app = Flask(__name__)

# Load model saat aplikasi startup
model = load_model('face_recognition_cnn.h5')
classes = {0: "Nesha", 1: "Syauqi"}

def predict_face(image_data):
    try:
        # Konversi base64 ke image
        img_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_bytes))
        
        # Konversi PIL Image ke OpenCV format
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        if img is None:
            return {"error": "Invalid image file"}

        # Preprocessing image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (160, 160))
        img = np.expand_dims(img, axis=0) / 255.0

        # Prediksi
        prediction = model.predict(img)
        predicted_class = int(np.argmax(prediction, axis=1)[0])
        
        return {"prediction": classes.get(predicted_class, "Unknown")}
    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['POST'])
def handle_prediction():
    if 'image' not in request.json:
        return jsonify({"error": "No image data provided"}), 400
    
    image_data = request.json['image']
    result = predict_face(image_data)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
