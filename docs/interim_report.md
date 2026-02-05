# Interim Report: Brent Oil Price Analysis

## Data Analysis Workflow
1. **Data Acquisition & Preprocessing**: Load historical Brent oil prices, handle missing values, and format dates.
2. **Exploratory Data Analysis (EDA)**: Perform stationarity tests (ADF), volatility analysis, and trend visualization.
3. **Event Research**: Map historical geopolitical/economic events to the timeline.
4. **Bayesian Modeling**: Use PyMC to implement a Change Point model (Switch point) to identify structural breaks.
5. **Validation & Interpretation**: Check MCMC convergence and quantify the mean price shift before and after detected points.
6. **Dashboard Development**: Integrate results into a Flask API and React dashboard.
## Assumptions and Limitations
- **Stationarity**: Prices are assumed to follow specific distributions (e.g., Normal or Poisson) within a regime, despite overall non-stationarity.
- **Causality vs. Correlation**: Statistical detection of a change point near an event suggests correlation, not definitive proof of cause-effect.
- **Data Frequency**: Daily data may not capture intraday shocks or delayed policy impacts.
- **External Factors**: The model focuses on price shifts but may miss the influence of secondary economic indicators like inflation or GDP.
## Communication Channels
- **Stakeholders**: Strategic reports for Birhan Energies' executive leadership.
- **Technical Teams**: GitHub repository documentation and Jupyter notebooks.
- **Public/Analysts**: An interactive React dashboard and a final blog post/technical report.