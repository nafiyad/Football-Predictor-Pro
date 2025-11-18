# ⚽ Football Predictor Pro

**Developer:** Nafiyad Adane

A professional-grade desktop application for football match predictions using ensemble machine learning models. Built entirely with Python and featuring a modern, intuitive GUI.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

### Core Functionality
- **Ensemble ML Predictions**: Combines XGBoost, LightGBM, and Random Forest models for accurate predictions
- **Multiple Markets**: 1X2 (Match Result), Both Teams To Score (BTTS), Over/Under 2.5 Goals
- **Historical Data Analysis**: Analyzes team form, head-to-head records, and performance metrics
- **Backtesting**: Evaluate model accuracy on historical data
- **Betting Tracker**: Track your bets, calculate ROI, and monitor performance
- **League Tables**: View standings and team statistics
- **Modern GUI**: Beautiful, responsive interface with dark/light themes

### Technical Features
- **100% Python**: No web browser required, native desktop application
- **Offline Capable**: Works completely offline with local data
- **SQLite Database**: Fast, reliable local data storage
- **Feature Engineering**: Advanced statistical features for ML models
- **Confidence Scoring**: Know how confident the model is in each prediction

## 📋 Requirements

- Python 3.9 or higher
- Windows, macOS, or Linux
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

## 🚀 Quick Start

### 1. Install Python
Download and install Python 3.9+ from [python.org](https://www.python.org/downloads/)

### 2. Clone or Download
```bash
git clone <repository-url>
cd football-prediction
```

Or download and extract the ZIP file.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database
This creates the database and populates it with 3 years of historical match data:

```bash
python scripts/seed_database.py
```

**Note**: This will take a few minutes to generate realistic historical data.

### 5. Train ML Models
Train the machine learning models on the historical data:

```bash
python scripts/train_all_models.py
```

**Note**: Training may take 5-15 minutes depending on your hardware.

### 6. Run the Application
```bash
python run.py
```

Or:

```bash
python src/main.py
```

## 📖 User Guide

### Dashboard
- View overall statistics (accuracy, ROI, win rate)
- See upcoming matches
- Quick access to predictions

### Matches
- Browse all matches (upcoming and finished)
- Filter by status
- Click any match to see detailed predictions

### Predictions
- View all generated predictions
- See confidence levels
- Recommended betting odds

### Statistics
- League tables and standings
- Team statistics and form
- Performance metrics

### Accuracy
- Backtest model performance
- View accuracy by confidence level
- ROI simulation with flat stakes

### Tracker
- Log your bets
- Track profit/loss
- Calculate ROI
- View betting history

### Settings
- Toggle dark/light theme
- View app information
- Database and model locations

## 🏗️ Project Structure

```
football-prediction/
├── src/
│   ├── main.py                 # Application entry point
│   ├── gui/                    # GUI components and pages
│   ├── models/                 # Database models
│   ├── services/               # Business logic services
│   ├── ml/                     # ML models and training
│   ├── database/               # Database setup and seeding
│   └── utils/                  # Utilities and configuration
├── data/
│   └── seed/                   # Seed data (leagues, teams)
├── scripts/                    # Setup and utility scripts
├── requirements.txt            # Python dependencies
├── run.py                      # Simple run script
└── README.md                   # This file
```

## 🤖 Machine Learning Models

### Models Used
1. **XGBoost Classifier**: Gradient boosting for 1X2 and BTTS predictions
2. **LightGBM Classifier**: Fast gradient boosting for 1X2 predictions
3. **Random Forest**: Ensemble decision trees for 1X2 and O/U 2.5

### Features
The models use 25 engineered features including:
- Team form (last 10 matches)
- Home/away performance splits
- Goals scored/conceded averages
- Win/draw/loss rates
- Clean sheet rates
- Expected Goals (xG) metrics
- Head-to-head history
- Recent form indicators

### Ensemble Method
Predictions are combined using weighted averaging:
- XGBoost: 35%
- LightGBM: 35%
- Random Forest: 30%

## 🗄️ Database Schema

### Main Tables
- **leagues**: Football leagues (Premier League, La Liga, etc.)
- **teams**: Teams with stadium and founding info
- **matches**: Match fixtures and results
- **match_stats**: Detailed match statistics (possession, shots, xG)
- **predictions**: ML model predictions
- **user_bets**: Betting tracker records

## 🎨 Customization

### Themes
Toggle between dark and light themes using the switch in the navigation sidebar.

### Configuration
Edit `src/utils/config.py` to customize:
- Window size
- ML model weights
- Feature engineering parameters
- Confidence thresholds

## 🐛 Troubleshooting

### "No matches found"
- Run `python scripts/seed_database.py` to populate the database

### "Models not loaded"
- Run `python scripts/train_all_models.py` to train the models

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### GUI doesn't appear
- Make sure you're not running in a headless environment
- Try: `pip install --upgrade customtkinter`

## 📊 Performance

### Typical Accuracy
- **1X2 Predictions**: 50-55% (better than random ~33%)
- **BTTS**: 60-65%
- **Over/Under 2.5**: 58-63%

**Note**: Accuracy depends on the quality and quantity of historical data.

### Backtesting
Use the Accuracy page to run backtests on historical data and see how the models would have performed.

## 🔄 Updating Data

### Add More Historical Data
1. Edit `data/seed/historical_matches.csv`
2. Run `python scripts/seed_database.py`
3. Retrain models: `python scripts/train_all_models.py`

### Add New Leagues/Teams
1. Edit `data/seed/leagues.json` and `data/seed/teams.json`
2. Run the seeding script again

## 🛠️ Development

### Tech Stack
- **GUI**: CustomTkinter (modern Tkinter wrapper)
- **Database**: SQLite with SQLAlchemy ORM
- **ML**: scikit-learn, XGBoost, LightGBM
- **Data**: pandas, numpy
- **Visualization**: matplotlib (for future charts)

### Adding New Features
1. Create new service in `src/services/`
2. Add GUI page in `src/gui/pages/`
3. Register page in `src/gui/app.py`
4. Add navigation button in `src/gui/components/navigation.py`

## 📝 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This application is for educational and entertainment purposes only. Predictions are based on historical data and statistical models, which cannot guarantee future results. Always gamble responsibly and never bet more than you can afford to lose.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For issues and questions, please open an issue on the repository.

## 🎯 Roadmap

- [ ] Live match updates
- [ ] More leagues and competitions
- [ ] Advanced visualizations and charts
- [ ] Export predictions to Excel/PDF
- [ ] Player-level statistics
- [ ] Injury and suspension tracking
- [ ] Weather data integration
- [ ] Mobile companion app

---

**Made with ⚽ and 🐍 by Nafiyad Adane**
