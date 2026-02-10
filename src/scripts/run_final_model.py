import pymc as pm
import numpy as np
import arviz as az
import pandas as pd
import json
import os

# --- THE MODEL CLASS (Built-in to avoid import errors) ---
class ChangePointModel:
    def __init__(self, data_series):
        # Weekly resampling for performance and stability
        self.data_series = data_series.resample('W').mean().dropna() if len(data_series) > 500 else data_series
        self.data = self.data_series.values
        self.dates = self.data_series.index
        self.n = len(self.data)
        self.trace = None

    def run_inference(self, samples=1000, tune=1000):
        with pm.Model() as model:
            tau = pm.DiscreteUniform("tau", lower=0, upper=self.n - 1)
            mu_1 = pm.Normal("mu_1", mu=self.data.mean(), sigma=self.data.std() * 2)
            mu_2 = pm.Normal("mu_2", mu=self.data.mean(), sigma=self.data.std() * 2)
            sigma = pm.HalfNormal("sigma", sigma=self.data.std())
            idx = np.arange(self.n)
            mu_switch = pm.math.switch(tau > idx, mu_1, mu_2)
            pm.Normal("obs", mu=mu_switch, sigma=sigma, observed=self.data)
            
            # Running with 2 chains as requested for diagnostics
            self.trace = pm.sample(samples, tune=tune, chains=2, cores=1, progressbar=True)
        return self.trace

    def get_diagnostics(self):
        if self.trace is None: return None
        summary = az.summary(self.trace, var_names=["tau", "mu_1", "mu_2"])
        is_converged = all(summary['r_hat'] < 1.05)
        return summary, is_converged

    def quantify_impact(self):
        tau_samples = self.trace.posterior["tau"].values.flatten()
        tau_mode = int(np.bincount(tau_samples).argmax())
        mu1_mean = self.trace.posterior["mu_1"].mean().values
        mu2_mean = self.trace.posterior["mu_2"].mean().values
        pct_change = ((mu2_mean - mu1_mean) / mu1_mean) * 100
        return {
            "date": self.dates[tau_mode].strftime('%d-%m-%Y'), # Format to match your sidebar
            "before_avg": round(float(mu1_mean), 2),
            "after_avg": round(float(mu2_mean), 2),
            "pct_change": f"{round(float(pct_change), 2)}%"
        }

# --- THE RUNNER LOGIC ---
if __name__ == "__main__":
    # 1. Load Data (assuming you are running from project root)
    data_path = 'data/BrentOilPrices.csv'
    df = pd.read_csv(data_path, parse_dates=['Date'], dayfirst=True)
    df.set_index('Date', inplace=True)
    
    print("🚀 Starting Robust Bayesian Inference (2 chains)...")
    model = ChangePointModel(df['Price'])
    model.run_inference()
    
    # 2. Print Diagnostics for your report
    summary, converged = model.get_diagnostics()
    print(f"\n✅ Model Converged (R-hat < 1.05): {converged}")
    print(summary[['mean', 'r_hat']])
    
    # 3. Save results for the Dashboard
    impact = model.quantify_impact()
    with open('data/model_results.json', 'w') as f:
        json.dump(impact, f)
    
    print(f"\n📊 Systematic Quantification saved to data/model_results.json")
    print(f"Detected Change Point: {impact['date']} | Impact: {impact['pct_change']}")