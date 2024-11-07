from flask import Flask, request, jsonify
import pickle
from PIL import Image
import numpy as np
import io

# Initialize the Flask application
app = Flask(__name__)

# Load the pre-trained model
with open('meta_model.pkl', 'rb') as model_file:
    meta_model = pickle.load(model_file)

# Preprocessing function for the image
def preprocess_image(image):
    # Resize, normalize, or preprocess image as your model expects
    image = image.resize((224, 224))  # Example resizing
    image_array = np.array(image) / 255.0  # Normalize if required by model
    image_array = image_array.reshape(1, -1)  # Adjust shape for prediction
    return image_array

# Endpoint for predicting food item
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Open and preprocess the image
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image)
        
        # Predict using the model
        prediction = meta_model.predict(processed_image)
        food_item_name = prediction[0]  # Assuming the model outputs the food name
        
        # Print the food item name in the console
        print(f"Predicted food item: {food_item_name}")
        
        return jsonify({"food_item": food_item_name})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
