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

    def preprocess_image(self, image_file, face_pos=(50, 50), target_size=(112, 112)):
        """Convert uploaded file to preprocessed numpy array"""
        
        img = Image.open(image_file.stream)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Get image dimensions
        height, width = img.shape[:2]  # More intuitive unpacking
        crop_width, crop_height = target_size

        # Validate face position
        x0, y0 = face_pos
        if x0 < 0 or y0 < 0:
            raise ValueError("Face position cannot be negative")
        
        # Calculate crop boundaries with safety checks
        x1 = min(x0 + crop_width, width)  # Prevent exceeding image width
        y1 = min(y0 + crop_height, height)  # Prevent exceeding image height
        
        # Adjust starting position if crop would exceed boundaries
        if x1 - x0 < crop_width:
            x0 = max(0, x1 - crop_width)
        if y1 - y0 < crop_height:
            y0 = max(0, y1 - crop_height)

        # Perform the crop
        cropped = img[y0:y1, x0:x1]  # Note: OpenCV uses row-major (y,x) ordering
        
        # Resize if the crop was smaller than target (edge case)
        if cropped.shape[0] != crop_height or cropped.shape[1] != crop_width:
            cropped = cv2.resize(cropped, target_size, interpolation=cv2.INTER_AREA)

        return np.expand_dims(cropped, axis=0) / 255.0
    
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

    def embed(self, image_file, face_pos=(50, 50)):
        """Main prediction method"""
        try:
            processed_img = self.preprocess_image(image_file, face_pos)
            prediction = self.model.predict(processed_img)
            predicted_class = int(np.argmax(prediction, axis=1)[0])

            return prediction[0].tolist()
        except Exception as e:
            return {"error here": str(e)}