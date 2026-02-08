import pandas as pd
import os

def load_and_preprocess_data(file_path):
    """Loads Brent Oil data, handles errors, and returns a cleaned DataFrame."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at: {file_path}")
        
        df = pd.read_csv(file_path)
        # Handle Date conversion with error catching
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        
        if df['Date'].isnull().any():
            print("Warning: Some dates could not be parsed and were removed.")
            df = df.dropna(subset=['Date'])
            
        df = df.sort_values('Date').set_index('Date')
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_log_returns(df, column='Price'):
    """Calculates log returns for stationarity."""
    import numpy as np
    return np.log(df[column] / df[column].shift(1)).dropna()