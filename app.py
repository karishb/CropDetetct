from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import base64
import io
from PIL import Image
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React Native app

# Load the model once when the app starts
model = None

def load_model():
    """Load the trained model"""
    global model
    try:
        # Try to download model if it doesn't exist
        if not os.path.exists('plant_detection_model.h5'):
            print("Model file not found. Attempting to download...")
            try:
                from download_model import download_model
                download_model()
            except Exception as e:
                print(f"Failed to download model: {e}")
                return False
        
        model = tf.keras.models.load_model('plant_detection_model.h5')
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        return False
    return True

# Class names for the model output
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

def preprocess_image(image_data):
    """Preprocess image for model prediction"""
    try:
        # Convert base64 to PIL Image
        if isinstance(image_data, str):
            # Remove data URL prefix if present
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            image = Image.open(image_data)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to 128x128
        image = image.resize((128, 128))
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_disease(image_array):
    """Predict disease using the loaded model"""
    try:
        if model is None:
            return None, "Model not loaded"
        
        # Make prediction
        predictions = model.predict(image_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_index])
        
        # Get class name
        predicted_class = CLASS_NAMES[predicted_class_index]
        
        return {
            'class': predicted_class,
            'confidence': confidence,
            'class_index': int(predicted_class_index)
        }
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None, str(e)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict disease from uploaded image"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'error': 'Model not loaded',
                'status': 'error'
            }), 500
        
        # Get image data from request
        if 'image' not in request.files and 'image_data' not in request.json:
            return jsonify({
                'error': 'No image provided',
                'status': 'error'
            }), 400
        
        # Handle file upload
        if 'image' in request.files:
            image_file = request.files['image']
            image_array = preprocess_image(image_file)
        else:
            # Handle base64 encoded image
            image_data = request.json['image_data']
            image_array = preprocess_image(image_data)
        
        if image_array is None:
            return jsonify({
                'error': 'Failed to process image',
                'status': 'error'
            }), 400
        
        # Make prediction
        result = predict_disease(image_array)
        
        if isinstance(result, tuple):
            return jsonify({
                'error': result[1],
                'status': 'error'
            }), 500
        
        return jsonify({
            'prediction': result,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/classes', methods=['GET'])
def get_classes():
    """Get list of supported classes"""
    return jsonify({
        'classes': CLASS_NAMES,
        'total_classes': len(CLASS_NAMES)
    })

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        print("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Failed to load model. Exiting...") 