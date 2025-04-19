from flask import Flask, request, jsonify
import pandas as pd
import pickle
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load the model and scaler
try:
    with open('model.pkl', 'rb') as f:
        model, scaler = pickle.load(f)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

# Load airports data
try:
    airports = pd.read_csv('airports.csv')
    logger.info(f"Loaded {len(airports)} airports")
except Exception as e:
    logger.error(f"Error loading airports data: {e}")
    raise

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Flight delay prediction API"})

@app.route('/airports')
def get_airports():
    logger.debug("Getting airports list")
    return jsonify(airports.to_dict(orient='records'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        logger.debug(f"Received prediction request: {request.json}")
        data = request.json
        
        day_of_week = int(data['dayOfWeek'])
        airport_id = int(data['airportId'])
        
        # Create feature DataFrame with exact column names and order
        feature_data = {
            'DestAirportID': [airport_id],
        }
        # Add one-hot encoded day of week columns in correct order
        for i in range(1, 8):
            feature_data[f'DayOfWeek_{i}'] = [1 if i == day_of_week else 0]
            
        features = pd.DataFrame(feature_data)
        
        # Ensure correct column order
        columns = ['DestAirportID'] + [f'DayOfWeek_{i}' for i in range(1, 8)]
        features = features[columns]
        
        logger.debug(f"Features created: {features.to_dict()}")
        
        # Scale features
        scaled_features = scaler.transform(features)
        
        # Make prediction
        probability = model.predict_proba(scaled_features)[0][1]
        
        response = {'probability': float(probability)}
        logger.info(f"Prediction made successfully: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)