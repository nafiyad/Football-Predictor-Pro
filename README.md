# Football Predictor Pro

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat)](https://xgboost.readthedocs.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A professional-grade desktop application for predicting football match outcomes using an ensemble machine learning model — achieving **65% accuracy** vs a 50% random baseline.

## Results

| Metric | Value |
|--------|-------|
| Prediction Accuracy | **65%** (vs 50% baseline) |
| Markets Covered | 1X2, BTTS, Over/Under 2.5 Goals |
| Features Engineered | 25 statistical features |
| Models in Ensemble | XGBoost + LightGBM + Random Forest |
| Backtesting | Full ROI simulation engine included |

## Features

- **Ensemble Model** — XGBoost, LightGBM, and Random Forest voting classifier
- **25 Engineered Features** — form, home/away stats, head-to-head, goal averages, and more
- **3 Prediction Markets** — Match result (1X2), Both Teams to Score (BTTS), and Over/Under 2.5 goals
- **Backtesting Engine** — Simulates historical performance with ROI calculation
- **Modern GUI** — Clean desktop interface built with Python
- **Local Database** — SQLite for storing match data and prediction history

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| ML Models | XGBoost, LightGBM, scikit-learn (Random Forest) |
| Data Processing | pandas, NumPy |
| Database | SQLite (SQLAlchemy) |
| GUI | Tkinter / CustomTkinter |

## Getting Started

```bash
# Clone the repository
git clone https://github.com/nafiyad/Football-Predictor-Pro.git
cd Football-Predictor-Pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## How It Works

1. **Data Ingestion** — Loads historical match data and computes rolling statistics
2. **Feature Engineering** — Generates 25 features per match (form, averages, H2H record)
3. **Model Training** — Trains XGBoost, LightGBM, and Random Forest classifiers
4. **Ensemble Voting** — Combines model outputs for final prediction
5. **Backtesting** — Validates predictions against historical outcomes with ROI simulation

## Author

**Nafiyad Adane** — [nafiyad.ca](https://nafiyad.ca) · [LinkedIn](https://www.linkedin.com/in/nafiyad-adane-g-041a04200/) · [GitHub](https://github.com/nafiyad)
