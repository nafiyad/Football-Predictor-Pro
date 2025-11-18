# 📦 Installation Guide

Complete installation guide for Football Predictor Pro on Windows, macOS, and Linux.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Python Installation](#python-installation)
3. [Project Setup](#project-setup)
4. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB
- **Storage**: 500MB free space
- **Python**: 3.9 or higher

### Recommended Requirements
- **RAM**: 8GB or more
- **Storage**: 1GB free space
- **Python**: 3.10 or 3.11

---

## Python Installation

### Windows

1. **Download Python**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.11 (or latest 3.x version)

2. **Install Python**
   - Run the installer
   - ✅ **IMPORTANT**: Check "Add Python to PATH"
   - Click "Install Now"

3. **Verify Installation**
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.x` or similar

### macOS

1. **Using Homebrew (Recommended)**
   ```bash
   # Install Homebrew if not installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python@3.11
   ```

2. **Or Download from python.org**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download macOS installer
   - Run the installer

3. **Verify Installation**
   ```bash
   python3 --version
   ```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Verify installation
python3.11 --version
```

---

## Project Setup

### Step 1: Download the Project

**Option A: Using Git**
```bash
git clone <repository-url>
cd football-prediction
```

**Option B: Download ZIP**
1. Download the ZIP file
2. Extract to a folder
3. Open terminal/command prompt in that folder

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- customtkinter (GUI framework)
- SQLAlchemy (database)
- scikit-learn, XGBoost, LightGBM (ML models)
- pandas, numpy (data processing)
- And other dependencies

**Expected time**: 2-5 minutes depending on internet speed

### Step 4: Verify Setup

```bash
python scripts/check_setup.py
```

This will check:
- ✓ All dependencies installed
- ✓ Database structure
- ✓ ML models

### Step 5: Seed Database

```bash
python scripts/seed_database.py
```

**What happens:**
- Creates SQLite database
- Adds 5 leagues (Premier League, La Liga, etc.)
- Adds 50 teams
- Generates 3 years of historical matches (~2700 matches)
- Creates upcoming fixtures (~75 matches)

**Expected time**: 3-5 minutes

### Step 6: Train ML Models

```bash
python scripts/train_all_models.py
```

**What happens:**
- Extracts features from historical data
- Trains 5 ML models (XGBoost, LightGBM, Random Forest)
- Saves models to disk

**Expected time**: 5-15 minutes (varies by hardware)

### Step 7: Run the Application

```bash
python run.py
```

The application window should open! 🎉

---

## Troubleshooting

### Issue: "python is not recognized" (Windows)

**Solution:**
1. Reinstall Python with "Add to PATH" checked
2. Or add Python manually to PATH:
   - Search "Environment Variables" in Windows
   - Edit PATH variable
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311`

### Issue: "pip is not recognized"

**Solution:**
```bash
python -m pip install --upgrade pip
```

### Issue: "No module named 'customtkinter'"

**Solution:**
```bash
pip install customtkinter
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: TensorFlow installation fails

**Solution:**
TensorFlow is optional. You can comment it out in `requirements.txt` if you encounter issues:
```
# tensorflow==2.15.0
```

The app will work without it (LSTM model won't be available, but other models will work).

### Issue: "Permission denied" (macOS/Linux)

**Solution:**
```bash
chmod +x scripts/*.py
python3 scripts/seed_database.py
```

### Issue: GUI doesn't appear

**Solutions:**
1. Make sure you're not in a headless/SSH environment
2. Update CustomTkinter:
   ```bash
   pip install --upgrade customtkinter
   ```
3. Check if tkinter is installed:
   ```bash
   python -m tkinter
   ```
   If error, install tkinter:
   - Ubuntu: `sudo apt install python3-tk`
   - macOS: Should be included with Python

### Issue: Database locked

**Solution:**
Close any other instances of the app, then:
```bash
# Delete database and reseed
rm src/database/predictions.db
python scripts/seed_database.py
```

### Issue: Low model accuracy

**This is normal!** Football is inherently unpredictable. Accuracy of 50-55% on 1X2 predictions is actually good (random guessing would be ~33%).

To improve:
- Add more historical data
- Increase training data quality
- Adjust model parameters in `src/ml/train_models.py`

### Issue: Slow performance

**Solutions:**
1. Close other applications
2. Reduce data:
   - Edit `src/database/seed_data.py`
   - Change `years=3` to `years=1` in `seed_historical_matches()`
3. Use fewer models:
   - Edit `src/services/prediction_service.py`
   - Remove models from ensemble

---

## Updating the Application

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Reset Database
```bash
python scripts/seed_database.py
```
Answer "yes" when prompted to clear existing data.

### Retrain Models
```bash
python scripts/train_all_models.py
```

---

## Uninstallation

### Remove Virtual Environment
```bash
# Deactivate first
deactivate

# Remove venv folder
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

### Remove Application
Simply delete the project folder.

### Remove Python (Optional)
- **Windows**: Use "Add or Remove Programs"
- **macOS**: `brew uninstall python@3.11`
- **Linux**: `sudo apt remove python3.11`

---

## Next Steps

After successful installation:

1. **Read the Quick Start Guide**: `QUICKSTART.md`
2. **Explore the application**: Start with the Dashboard
3. **Generate predictions**: Go to Matches → Click a match → Predict
4. **Run backtests**: Go to Accuracy → Select period → Run Backtest
5. **Check the README**: `README.md` for full documentation

---

## Getting Help

If you encounter issues not covered here:

1. Check the console/terminal for error messages
2. Look in `logs/` directory for detailed logs
3. Run the setup check: `python scripts/check_setup.py`
4. Open an issue on the repository with:
   - Your OS and Python version
   - Error message
   - Steps to reproduce

---

**Happy Predicting! ⚽**



