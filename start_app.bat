@echo off
echo.
echo ========================================
echo   Football Predictor Pro
echo ========================================
echo.
echo Starting application...
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   Error starting application!
    echo ========================================
    echo.
    echo Please check:
    echo 1. Python is installed
    echo 2. Dependencies are installed: pip install -r requirements.txt
    echo 3. Database is seeded: python scripts\seed_database.py
    echo 4. Models are trained: python scripts\train_all_models.py
    echo.
    pause
)



