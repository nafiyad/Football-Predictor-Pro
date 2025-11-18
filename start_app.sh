#!/bin/bash

echo ""
echo "========================================"
echo "  Football Predictor Pro"
echo "========================================"
echo ""
echo "Starting application..."
echo ""

python3 run.py

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  Error starting application!"
    echo "========================================"
    echo ""
    echo "Please check:"
    echo "1. Python 3.9+ is installed"
    echo "2. Dependencies are installed: pip install -r requirements.txt"
    echo "3. Database is seeded: python3 scripts/seed_database.py"
    echo "4. Models are trained: python3 scripts/train_all_models.py"
    echo ""
    read -p "Press Enter to continue..."
fi



