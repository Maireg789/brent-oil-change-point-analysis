from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allows React to talk to this API

# Helper to load data - adjust path based on your 'data' folder
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/BrentOilPrices.csv')

@app.route('/api/prices', methods=['GET'])
def get_prices():
    try:
        df = pd.read_csv(DATA_PATH)
        # Convert to list of dicts for JSON: [{"Date": "...", "Price": ...}, ...]
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    