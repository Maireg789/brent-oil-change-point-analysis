import pymc as pm
import numpy as np
import arviz as az
import pandas as pd

class ChangePointModel:
    def __init__(self, data_series):
        # OPTIMIZATION: Resample to Weekly if data is too large (>500 points)
        if len(data_series) > 500:
            self.data_series = data_series.resample('W').mean().dropna()
        else:
            self.data_series = data_series
            
        self.data = self.data_series.values
        self.dates = self.data_series.index
        self.n = len(self.data)
        self.model = None
        self.trace = None

    def run_inference(self, samples=500, tune=500):
        if self.n < 10: return None # Not enough data
        
        with pm.Model() as self.model:
            tau = pm.DiscreteUniform("tau", lower=0, upper=self.n - 1)
            mu_1 = pm.Normal("mu_1", mu=self.data.mean(), sigma=self.data.std() * 2)
            mu_2 = pm.Normal("mu_2", mu=self.data.mean(), sigma=self.data.std() * 2)
            sigma = pm.HalfNormal("sigma", sigma=self.data.std())
            
            idx = np.arange(self.n)
            mu_switch = pm.math.switch(tau > idx, mu_1, mu_2)
            
            observation = pm.Normal("obs", mu=mu_switch, sigma=sigma, observed=self.data)
            
            # Fast settings for Windows
            self.trace = pm.sample(samples, tune=tune, chains=1, cores=1, progressbar=False)
        return self.trace

    def get_change_point_date(self):
        if self.trace is None: return None, None
        
        tau_samples = self.trace.posterior["tau"].values.flatten()
        tau_mode = int(np.bincount(tau_samples).argmax())
        
        # Return the Date and the Index
        return self.dates[tau_mode], tau_mode