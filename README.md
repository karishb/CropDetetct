# Plant Disease Detection API

A Flask-based REST API for plant disease detection using a trained deep learning model. This API can be integrated with React Native applications to provide real-time plant disease detection.

## Features

- 🚀 Fast prediction using pre-trained CNN model
- 📱 Compatible with React Native apps
- 🔄 Supports both file upload and base64 encoded images
- 🌐 CORS enabled for cross-origin requests
- 📊 Health check and monitoring endpoints
- 🐳 Docker support for easy deployment

## API Endpoints

### 1. Health Check
```
GET /health
```
Returns the health status of the API and model.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Get Supported Classes
```
GET /classes
```
Returns list of all supported plant disease classes.

**Response:**
```json
{
  "classes": ["Apple___Apple_scab", "Apple___Black_rot", ...],
  "total_classes": 38
}
```

### 3. Predict Disease
```
POST /predict
```

**Request Options:**

**Option 1: File Upload**
```javascript
// React Native example
const formData = new FormData();
formData.append('image', {
  uri: imageUri,
  type: 'image/jpeg',
  name: 'plant.jpg'
});

fetch('YOUR_API_URL/predict', {
  method: 'POST',
  body: formData
});
```

**Option 2: Base64 Encoded Image**
```javascript
// React Native example
const response = await fetch('YOUR_API_URL/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    image_data: base64ImageString
  })
});
```

**Response:**
```json
{
  "prediction": {
    "class": "Tomato___healthy",
    "confidence": 0.95,
    "class_index": 37
  },
  "status": "success"
}
```

## Deployment Options

### Option 1: Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the API:**
```bash
python app.py
```

3. **Test the API:**
```bash
python test_api.py
```

### Option 2: Docker Deployment

1. **Build the Docker image:**
```bash
docker build -t plant-disease-api .
```

2. **Run the container:**
```bash
docker run -p 5000:5000 plant-disease-api
```

### Option 3: Cloud Deployment

#### Heroku
1. Create a `Procfile`:
```
web: gunicorn app:app
```

2. Deploy using Heroku CLI:
```bash
heroku create your-app-name
git add .
git commit -m "Initial commit"
git push heroku main
```

#### Railway
1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Dockerfile and deploy

#### Render
1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`

## React Native Integration

### Example React Native Code

```javascript
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const PlantDiseaseApp = () => {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = 'YOUR_API_URL'; // Replace with your deployed API URL

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  const predictDisease = async () => {
    if (!image) {
      Alert.alert('Error', 'Please select an image first');
      return;
    }

    setLoading(true);
    try {
      // Convert image to base64
      const response = await fetch(image);
      const blob = await response.blob();
      const base64 = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(blob);
      });

      // Send to API
      const apiResponse = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_data: base64
        })
      });

      const result = await apiResponse.json();
      
      if (result.status === 'success') {
        setPrediction(result.prediction);
      } else {
        Alert.alert('Error', result.error || 'Prediction failed');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to connect to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 20 }}>
        Plant Disease Detection
      </Text>
      
      <TouchableOpacity onPress={pickImage} style={{ marginBottom: 20 }}>
        <Text>Pick an image</Text>
      </TouchableOpacity>
      
      {image && (
        <Image source={{ uri: image }} style={{ width: 200, height: 200, marginBottom: 20 }} />
      )}
      
      <TouchableOpacity onPress={predictDisease} disabled={loading}>
        <Text>{loading ? 'Analyzing...' : 'Detect Disease'}</Text>
      </TouchableOpacity>
      
      {prediction && (
        <View style={{ marginTop: 20 }}>
          <Text>Disease: {prediction.class}</Text>
          <Text>Confidence: {(prediction.confidence * 100).toFixed(2)}%</Text>
        </View>
      )}
    </View>
  );
};

export default PlantDiseaseApp;
```

## Environment Variables

You can set the following environment variables:

- `PORT`: Port number (default: 5000)
- `MODEL_PATH`: Path to the model file (default: 'plant_detection_model.h5')

## Model Information

- **Architecture**: Convolutional Neural Network (CNN)
- **Input Size**: 128x128 RGB images
- **Classes**: 38 different plant diseases and healthy states
- **Model Size**: ~468MB

## Troubleshooting

### Common Issues

1. **Model loading fails:**
   - Ensure `plant_detection_model.h5` is in the same directory as `app.py`
   - Check if the model file is corrupted

2. **CORS errors in React Native:**
   - The API already has CORS enabled
   - Make sure your API URL is correct

3. **Memory issues:**
   - The model requires significant RAM (~2GB recommended)
   - Consider using a cloud service with adequate resources

4. **Slow predictions:**
   - First prediction might be slow due to model loading
   - Subsequent predictions should be faster
   - Consider using GPU acceleration for better performance

## License

This project is licensed under the MIT License. 