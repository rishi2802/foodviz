from flask import Flask, render_template, request, jsonify
from inference_sdk import InferenceHTTPClient
from PIL import Image
import io
import os
import requests
import json

app = Flask(__name__, static_folder='static')

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="MLFbasW47mptS1MgzQZp"
)

def fetch_nutritional_data(food_item):
    api_key = 'f1d9ff764f44e2017e86da4174c34618'  # Replace with your actual API key
    app_id = '69a71a86'  # Replace with your actual App ID
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'

    headers = {
        'Content-Type': 'application/json',
        'x-app-id': app_id,
        'x-app-key': api_key
    }

    body = {
        'query': food_item
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    try:
        # Check if the file is an image
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({"error": "Invalid file type. Please upload an image."}), 400

        # Load and save the image temporarily
        image = Image.open(io.BytesIO(file.read()))
        image_path = os.path.join('static/uploads', file.filename)

        # Ensure the 'uploads' folder exists
        if not os.path.exists('static/uploads'):
            os.makedirs('static/uploads')

        image.save(image_path)
        
        # Send the image to Roboflow and get predictions
        result = CLIENT.infer(image_path, model_id="food-detection-yldun/1")

        # Log the response from Roboflow for debugging
        print(f"Roboflow response: {result}")  # Check if you get any error details here

        # Ensure the response contains predictions
        if 'predictions' not in result or not result['predictions']:
            return jsonify({"error": "No predictions found."}), 400

        # Extract food names from the response
        predictions = result['predictions']
        food_names = [prediction['class'] for prediction in predictions]

        # For simplicity, using the first detected food name
        predicted_food = food_names[0] if food_names else "Unknown food"

        # Constructing the response data with dummy nutritional and allergen data
        response_data = {
            "foodName": predicted_food,
            "nutritionData": [
                {"nutrient": "Protein", "value": "3.5g"},
                {"nutrient": "Total Fat", "value": "17.2g"},
                {"nutrient": "Total Carbohydrates", "value": "24.0g"},
                {"nutrient": "Calories", "value": "261.5 kcal"}
            ],
            "allergenData": [
                {"allergen": "Peanuts", "sideEffects": "Anaphylaxis, hives, swelling"},
                {"allergen": "Soy", "sideEffects": "Respiratory issues, skin irritation"}
            ]
        }

        return jsonify(response_data)

    except Exception as e:
        # Log the full exception
        print(f"Error processing the image: {e}")

        # Return a detailed error message to the frontend
        return jsonify({"error": f"There was an issue processing the image. Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
