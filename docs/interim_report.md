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
## Change Point Models
- **Purpose**: To identify structural breaks where the underlying statistical properties (mean, variance) of the price series change significantly.
- **Expected Outputs**: 
    - **Tau ($\tau$)**: The estimated date/index of the switch point.
    - **$\mu_1, \mu_2$**: The mean price parameters before and after the shift.
    - **Uncertainty**: Posterior distributions showing the model's confidence in the detected date.
    ## Time Series Properties Investigation
- **Trend Analysis**: Identifying long-term upward or downward movements using rolling averages.
- **Stationarity Testing**: Applying the Augmented Dickey-Fuller (ADF) test to determine if the series needs differencing (e.g., Log Returns).
- **Volatility Patterns**: Using log-return plots to identify "volatility clustering," where high-volatility periods follow each other, informing the choice of likelihood distribution.
## Initial EDA Findings
- **Non-Stationarity**: The raw Brent oil price series is non-stationary (ADF p-value > 0.05), while the Log Returns are stationary, making them suitable for volatility analysis.
- **Volatility Clustering**: Significant spikes in volatility were observed around 2008 (Financial Crisis), 2020 (COVID-19), and 2022 (Russia-Ukraine war).
- **Event Correlation**: Visual inspection shows sharp price shifts following the 1990 Gulf War, the 2014 OPEC production decision, and the 2020 price war.
- **Trend**: A long-term upward trend is visible from 2002 to 2008, followed by high-frequency structural breaks in the last decade.
## Technical Improvements and Refinements
- **Structured Event Dataset**: Developed a standardized `data/events.csv` to map geopolitical events with specific dates and categorized impacts (Supply vs. Demand shocks).
- **Code Modularity**: Refactored core logic into `src/scripts/data_utils.py`, separating data processing from visualization notebooks for better maintainability.
- **Error Handling & Robustness**: Implemented robust data validation checks for file paths and date parsing to ensure a stable pipeline for Bayesian modeling.
- **Bayesian Modeling Progress**: Successfully implemented a PyMC Switch Point model to detect structural breaks in the Brent oil price series, identifying key dates of regime shifts.