# Birhan Energies: Brent Oil Price Analysis & Change Point Detection

This repository contains a full-stack data science application designed to identify, quantify, and visualize structural breaks in Brent crude oil prices (1987-2022) using Bayesian inference.

## 🚀 Project Overview
Birhan Energies specializes in energy sector insights. This project evaluates how major geopolitical events—such as OPEC decisions, regional conflicts, and global health crises—trigger fundamental shifts in oil market pricing.

### Key Deliverables:
- **Bayesian Change Point Model**: A robust PyMC-based model that detects structural breaks with MCMC convergence diagnostics (R-hat).
- **Quantified Impact Analysis**: Systematic calculation of price shifts (before vs. after) around detected events.
- **Interactive Dashboard**: A React (Vite) frontend and Flask API to visualize trends, detected breakpoints, and historical events.

---

## 📈 Key Findings (Quantified Insights)
The model identified a primary structural break on **March 11, 2020**, correlating with the **WHO COVID-19 Pandemic Declaration**.
- **Average Price Before**: $50.32
- **Average Price After**: $28.45
- **Quantified Impact**: **43.5% decrease** in mean price.
- **Model Rigor**: The MCMC chains achieved convergence with an **R-hat of 1.01**, confirming the statistical validity of the detected change point.

---

## 🛠️ Tech Stack
- **Analysis**: Python (PyMC, ArviZ, Pandas, NumPy)
- **Backend**: Flask, Flask-CORS
- **Frontend**: React (Vite), Recharts, Axios
- **Version Control**: Git (Branch-based workflow with PRs)

---

## 📁 Project Structure
```text
├── data/                  # Raw price CSVs, event data, and model results
├── src/
│   ├── api/               # Flask Backend API (app.py)
│   ├── scripts/           # Bayesian modeling and quantification scripts
│   └── notebooks/         # EDA and Model development notebooks
├── dashboard-ui/          # React (Vite) Frontend Application
└── docs/                  # Project reports and documentation
``` 
## ⚙️ Setup and Installation
1. Backend Setup
code
Powershell
# Navigate to root and activate venv
.\venv\Scripts\activate

# Start the Flask API
python src/api/app.py
2. Frontend Setup
code
Powershell
# Navigate to dashboard folder
cd dashboard-ui
npm install
npm run dev
## 📊 Methodology & Rigor
To address the complexity of 30+ years of data, this project implemented:
Convergence Diagnostics: Used ArviZ to calculate R-hat statistics, ensuring MCMC chains reached a stable posterior distribution.
Systematic Association: Developed an event-matching algorithm to correlate detected mathematical change points with a researched dataset of geopolitical events.
Weekly Resampling: Optimized the dataset for Bayesian inference to improve model stability and performance on Windows systems.
## 🤝 Team
Maireg - Lead Data Scientist
Tutors: Kerod, Filimon, Mahbubah