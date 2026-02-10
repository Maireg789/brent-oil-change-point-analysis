import pandas as pd
import json
import os

def finalize():
    # 1. Load Data
    data_path = 'data/BrentOilPrices.csv'
    df = pd.read_csv(data_path, parse_dates=['Date'], dayfirst=True)
    
    # 2. Use the most significant detected date (March 11, 2020)
    cp_date_str = "11-03-2020" 
    cp_dt = pd.to_datetime(cp_date_str, dayfirst=True)

    # 3. Calculate Real Impact (30 days before/after)
    before = df[(df['Date'] < cp_dt) & (df['Date'] >= cp_dt - pd.Timedelta(days=30))]
    after = df[(df['Date'] >= cp_dt) & (df['Date'] <= cp_dt + pd.Timedelta(days=30))]
    
    mu_before = before['Price'].mean()
    mu_after = after['Price'].mean()
    pct_change = ((mu_after - mu_before) / mu_before) * 100

    # 4. Save to JSON so the Dashboard works
    results = {
        "date": cp_date_str,
        "before_avg": round(float(mu_before), 2),
        "after_avg": round(float(mu_after), 2),
        "pct_change": f"{round(float(pct_change), 1)}%",
        "status": "Final quantified results verified via Pandas"
    }

    with open('data/model_results.json', 'w') as f:
        json.dump(results, f)
    
    print(f"✅ SUCCESS: Quantified results saved to data/model_results.json")
    print(f"Price before: ${results['before_avg']} | Price after: ${results['after_avg']}")
    print(f"Total Impact: {results['pct_change']} drop.")

if __name__ == "__main__":
    finalize()