import pickle
import json
from flask import Flask, request, jsonify

# 1. Load the trained AI model
try:
    with open('model.pkl', 'rb') as file:
        model_data = pickle.load(file)
    ai_model = model_data['model']
    label_encoder = model_data['encoder']
    print("AI Model loaded successfully.")
except FileNotFoundError:
    print("ERROR: model.pkl not found. Run train_model.py first.")
    # Create dummy model to prevent crash
    class DummyModel:
        def predict(self, X):
            return [0]
        def inverse_transform(self, y):
            return ['UNKNOWN']
    ai_model = DummyModel()
    label_encoder = DummyModel()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_courier():
    # Get data from the POST request (e.g., {"tracking_number": "123456789"})
    data = request.get_json(silent=True)
    if not data or 'tracking_number' not in data:
        return jsonify({"error": "Invalid input. 'tracking_number' field is required."}), 400

    tracking_number = data['tracking_number']

    # 2. Feature Engineering (must match the training script!)
    # The model only looks at the length of the tracking number
    number_length = len(str(tracking_number))

    # 3. Predict courier using the AI model
    # The model expects a list of lists, so we use [[number_length]]
    prediction_encoded = ai_model.predict([[number_length]])

    # 4. Convert numerical prediction back to text label (e.g., 0 -> DPD)
    predicted_courier = label_encoder.inverse_transform(prediction_encoded)[0]

    # 5. Return the result
    response = {
        "tracking_number": tracking_number,
        "predicted_courier": predicted_courier,
        "model_confidence": "Low (based only on length)" # Good practice to note model limitations
    }

    # NOTE: W REALNYM PROJEKCIE TUTAJ NASTĄPIŁOBY ODWOŁANIE DO API KURJERA

    return jsonify(response)

@app.route('/status', methods=['GET'])
def status_check():
    return jsonify({"status": "OK", "model_ready": "model.pkl" in globals()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')