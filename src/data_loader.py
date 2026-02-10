
import pandas as pd
import numpy as np
import os

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        self.data = pd.read_csv(self.file_path)
        # Try multiple date formats
        for fmt in ['%d-%b-%y', '%Y-%m-%d', '%d/%m/%Y']:
            try:
                self.data['Date'] = pd.to_datetime(self.data['Date'], format=fmt)
                break
            except:
                continue
        self.data.sort_values('Date', inplace=True)
        self.data.set_index('Date', inplace=True)
        self.data['Price'] = self.data['Price'].ffill()
        return self.data
