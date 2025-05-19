import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import json
import os

class FacePredictor:
    def __init__(self, model_path, classes_config=None):
        """
        Args:
            model_path: Path ke model .h5
            classes_config: Bisa berupa:
                - Path ke JSON file (str)
                - Dictionary langsung
                - None (gunakan default)
        """
        self.model = load_model(model_path)
        self.classes = self._load_classes(classes_config)
    
    def _load_classes(self, config):
        """Load class mapping dari berbagai sumber"""
        if config is None:
            return {0: "Nesha", 1: "Syauqi"}  # Default fallback
            
        if isinstance(config, str):
            # Load dari file JSON
            with open(config, 'r') as f:
                return json.load(f)
                
        elif isinstance(config, dict):
            # Gunakan langsung dictionary
            return config
            
        else:
            raise ValueError("Format classes_config tidak valid")

    def preprocess_image(self, image_file):
        """Convert uploaded file to preprocessed numpy array"""
        img = Image.open(image_file.stream)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        if img is None:
            raise ValueError("Invalid image file")
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (112, 112))
        return np.expand_dims(img, axis=0) / 255.0
    
    def predict(self, image_file):
        """Main prediction method"""
        try:
            processed_img = self.preprocess_image(image_file)
            prediction = self.model.predict(processed_img)
            predicted_class = int(np.argmax(prediction, axis=1)[0])

            # MASUKIN ini ke database
            print("embedding shape:", prediction.shape)
            print(":", prediction[:5])

            return {
                "prediction": self.classes.get(str(predicted_class), "Unknown"),
                "confidence": float(np.max(prediction)),
                "class_id": predicted_class,  # Tambahkan ID original
                "prediction_embed": prediction.tolist(),
            }
        except Exception as e:
            return {"error": str(e)}
