from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Absolute path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICES_CSV = os.path.abspath(os.path.join(BASE_DIR, '../../data/BrentOilPrices.csv'))
EVENTS_CSV = os.path.abspath(os.path.join(BASE_DIR, '../../data/event_data.csv'))

@app.route('/api/analysis-results', methods=['GET'])
def get_analysis():
    try:
        # 1. Load data to calculate impact
        df = pd.read_csv(PRICES_CSV)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        
        # 2. Define the detected change point (Result from your Task 2 model)
        # We use March 11, 2020 as the primary example for the COVID shock
        cp_date_str = "11-03-2020" 
        cp_date_ts = pd.to_datetime(cp_date_str, dayfirst=True)

        # 3. Calculate "Before" and "After" stats (The "Robust" part)
        # Look at 30 days before and after for a clean impact window
        before_mask = (df['Date'] < cp_date_ts) & (df['Date'] >= cp_date_ts - pd.Timedelta(days=30))
        after_mask = (df['Date'] >= cp_date_ts) & (df['Date'] <= cp_date_ts + pd.Timedelta(days=30))
        
        avg_before = df.loc[before_mask, 'Price'].mean()
        avg_after = df.loc[after_mask, 'Price'].mean()
        
        price_change = avg_after - avg_before
        percentage_change = (price_change / avg_before) * 100

        # 4. Return detailed JSON
        return jsonify({
            "status": "success",
            "change_point_date": cp_date_str,
            "metrics": {
                "avg_price_before": round(avg_before, 2),
                "avg_price_after": round(avg_after, 2),
                "absolute_change": round(price_change, 2),
                "percentage_change": f"{round(percentage_change, 2)}%"
            },
            "description": f"Model detected a structural break. Prices shifted from ${round(avg_before, 2)} to ${round(avg_after, 2)}."
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "fallback_date": "11-03-2020"
        }), 500

@app.route('/api/prices', methods=['GET'])
def get_prices():
    df = pd.read_csv(PRICES_CSV)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/events', methods=['GET'])
def get_events():
    if os.path.exists(EVENTS_CSV):
        df = pd.read_csv(EVENTS_CSV)
        return jsonify(df.to_dict(orient='records'))
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)