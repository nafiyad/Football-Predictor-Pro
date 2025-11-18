"""Simple run script for the application."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Run main application
from main import main

if __name__ == "__main__":
    main()



