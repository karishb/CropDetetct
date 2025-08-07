# Plant Detection Model Deployment Guide

## Essential Files for Deployment

The following files are required for the model to work on Render:

### Core Application Files
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Tells Render how to run the app
- `render.yaml` - Render deployment configuration

### Model Files
- `plant_detection_model.h5` - Your trained model (will be downloaded on deployment)
- `download_model.py` - Script to download the model if not present

### Optional Files
- `create_test_image.py` - For creating test images
- `test_api.py` - For testing the API
- `test_prediction.py` - For testing predictions

## Deployment Steps

1. **Prepare Your Repository**
   - Ensure only essential files are committed (use the updated .gitignore)
   - Make sure your model file is accessible for download

2. **Update Model Download**
   - Update `download_model.py` with your actual model download URL
   - You can host your model on:
     - Google Drive (get direct download link)
     - Dropbox
     - AWS S3
     - Any file hosting service

3. **Deploy to Render**
   - Connect your GitHub repository to Render
   - Render will automatically detect the Python environment
   - The app will be available at: `https://your-app-name.onrender.com`

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Predict plant disease from image
- `GET /classes` - Get list of supported classes

## Testing the Deployment

1. Health check: `GET https://your-app-name.onrender.com/health`
2. Test prediction: Send POST request to `/predict` with image data

## Important Notes

- The model file is excluded from git due to size
- The app will download the model on first startup
- Free tier has limitations on build time and memory
- Consider upgrading to paid plan for production use 