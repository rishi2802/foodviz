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



# Nutrient IDs to names mapping
important_nutrients = {
    208: 'Calories',
    203: 'Protein',
    204: 'Total Fat',
    205: 'Total Carbohydrates',
    269: 'Sugars',
    307: 'Sodium',
    291: 'Fiber',
    301: 'Calcium',
    303: 'Iron',
    304: 'Magnesium',
    305: 'Phosphorus',
    306: 'Potassium',
    401: 'Vitamin C',
    404: 'Vitamin B1 (Thiamin)',
    405: 'Vitamin B2 (Riboflavin)',
    406: 'Vitamin B3 (Niacin)',
    415: 'Vitamin B6',
    417: 'Folate',
    418: 'Vitamin B12',
    320: 'Vitamin A',
    323: 'Vitamin E',
    328: 'Vitamin D',
    430: 'Vitamin K'
}


# Predefined allergens and side effects for food items
food_allergens_and_effects = {
    "pancakes": {
        "allergens": ["Wheat", "Milk", "Eggs"],
        "sideEffects": "Anaphylaxis, hives, itching, swelling, gastrointestinal issues"
    },
    "club sandwich": {
        "allergens": ["Wheat", "Eggs", "Milk", "Soy", "Mustard"],
        "sideEffects": "Anaphylaxis, hives, itching, swelling, respiratory issues, gastrointestinal issues"
    },
    "samosa": {
        "allergens": ["Wheat", "Soy", "Milk", "Sesame"],
        "sideEffects": "Anaphylaxis, hives, itching, swelling, gastrointestinal issues"
    },
    "french fries": {
        "allergens": ["Wheat", "Soy"],  
        "sideEffects": "Hives, itching, swelling, gastrointestinal upset"
    },
    "macaroni and cheese": {
        "allergens": ["Wheat", "Milk", "Eggs"],
        "sideEffects": "Anaphylaxis, hives, itching, swelling, gastrointestinal issues"
    },
    "waffles": {
        "allergens": ["Wheat", "Milk", "Eggs"],
        "sideEffects": "Anaphylaxis, hives, itching, swelling, gastrointestinal issues"
    }
}


def get_allergens_and_side_effects(food_item):
    """Return allergens and side effects for the given food item."""
    if food_item in food_allergens_and_effects:
        return food_allergens_and_effects[food_item]
    else:
        return {
            "allergens": ["Unknown"],
            "sideEffects": "Unknown side effects"
        }

# Fetch nutritional data from Nutritionix API
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

        # Fetch nutritional data from Nutritionix API based on the detected food
        nutrition_data = fetch_nutritional_data(predicted_food)
        


        # Extract the relevant nutrients (nutrient names and values) from Nutritionix response
        nutrition_info = []
        for nutrient in nutrition_data['foods'][0]['full_nutrients']:
            # Map the attr_id to the nutrient name using important_nutrients dictionary
            nutrient_name = important_nutrients.get(nutrient.get('attr_id'))
            if nutrient_name:
                nutrition_info.append({
                    'nutrient': nutrient_name,
                    'value': nutrient.get('value')
                })
        # Fetch allergens and side effects for the predicted food
        allergen_data = get_allergens_and_side_effects(predicted_food)

        # Constructing the response data with the food name and nutritional info
        response_data = {
            "foodName": predicted_food,
            "nutritionData": nutrition_info,
            "allergenData": allergen_data
        }

        return jsonify(response_data)

    except Exception as e:
        # Log the full exception
        print(f"Error processing the image: {e}")

        # Return a detailed error message to the frontend
        return jsonify({"error": f"There was an issue processing the image. Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
