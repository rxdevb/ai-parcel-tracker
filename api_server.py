import pickle
import os
import sys
from flask import Flask, request, jsonify, Response
from typing import Dict, Any, Union, Tuple, Optional

# --- Configuration Constants ---
MODEL_PATH: str = os.environ.get('MODEL_PATH', 'model.pkl')
APP_NAME: str = "ai_parcel_tracker"

# Variables to hold the loaded model components
ai_model: Any
label_encoder: Any
model_metadata: Dict[str, Any] = {}


def load_ai_model() -> None:
    """Loads the serialized model components from the disk."""
    global ai_model, label_encoder, model_metadata

    try:
        with open(MODEL_PATH, 'rb') as file:
            model_data: Dict[str, Any] = pickle.load(file)

        ai_model = model_data['model']
        label_encoder = model_data['encoder']
        model_metadata = model_data.get('metadata', {})
        print(f"INFO: Model loaded. Training Date: {model_metadata.get('training_date', 'N/A')}")

    except FileNotFoundError:
        print(f"FATAL: Model file '{MODEL_PATH}' not found. Exiting.")
        sys.exit(1)
    except Exception as e:
        print(f"FATAL: Failed to deserialize model. Details: {e}. Exiting.")
        sys.exit(1)


# Initialize Flask application and load model on startup
load_ai_model()
app = Flask(APP_NAME)


@app.route('/predict', methods=['POST'])
def predict_courier() -> Tuple[Response, int]:
    """Endpoint for receiving a tracking number and returning a courier prediction."""

    # Get JSON payload from the request.
    data: Optional[Dict[str, Any]] = request.get_json(silent=True)

    # Input validation: check for key and expected type (str or int).
    tracking_number: Optional[Union[str, int]] = data.get('tracking_number') if data else None

    if tracking_number is None or not isinstance(tracking_number, (str, int)):
        return jsonify({
            "error": "Validation failed: 'tracking_number' field (string or integer) is required."
        }), 400

    # Feature Extraction: Apply the same length logic as used in training.
    number_length: int = len(str(tracking_number))

    # Model Inference: Predict the encoded label (requires 2D input structure).
    prediction_encoded = ai_model.predict([[number_length]])

    # Post-processing: Convert the numerical label back to the courier name.
    predicted_courier: str = label_encoder.inverse_transform(prediction_encoded)[0]

    # Formulate the response.
    response: Dict[str, Any] = {
        "tracking_number": str(tracking_number),
        "predicted_courier": predicted_courier,
        "model_note": "Prediction based solely on tracking number length."
    }

    return jsonify(response), 200


@app.route('/status', methods=['GET'])
def status_check() -> Tuple[Response, int]:
    """Health check endpoint to confirm service is running and model is loaded."""
    return jsonify({
        "status": "OK",
        "service": APP_NAME,
        "model_ready": True,
        "model_version": model_metadata.get('training_date', 'unknown')
    }), 200


if __name__ == '__main__':
    # Run the server. Use 0.0.0.0 for containerized environments.
    # NOTE: Use Gunicorn in production for robust service.
    app.run(debug=True, host='0.0.0.0', port=5001)