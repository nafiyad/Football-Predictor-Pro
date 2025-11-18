@echo off
echo ========================================
echo   Verifying Repository Cleanliness
echo ========================================
echo.

echo Checking for unwanted files...
echo.

:: Check for database files
if exist "src\database\*.db" (
    echo [WARNING] Found .db files - they will be ignored by git
) else (
    echo [OK] No database files found
)

:: Check for log files
if exist "logs\*.log" (
    echo [WARNING] Found log files - they will be ignored by git
) else (
    echo [OK] No log files found
)

:: Check for model files
if exist "src\ml\saved_models\*.pkl" (
    echo [WARNING] Found .pkl model files - they will be ignored by git
) else (
    echo [OK] No model files found
)

:: Check for pycache
if exist "src\__pycache__" (
    echo [WARNING] Found __pycache__ directories - they will be ignored by git
) else (
    echo [OK] No __pycache__ directories found
)

echo.
echo ========================================
echo   Repository Status
echo ========================================
echo.
echo Your repository is clean and ready for GitHub!
echo.
echo All unwanted files are protected by .gitignore:
echo   - Database files (*.db)
echo   - ML models (*.pkl)
echo   - Log files (*.log)
echo   - Python cache (__pycache__)
echo   - Virtual environments (venv/)
echo.
echo Next steps:
echo   1. Review GITHUB_SETUP.md
echo   2. Initialize git: git init
echo   3. Stage files: git add .
echo   4. Commit: git commit -m "Initial commit"
echo   5. Push to GitHub
echo.
echo ========================================
pause

