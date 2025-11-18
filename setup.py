"""
Football Predictor Pro - Setup Configuration
Author: Nafiyad Adane
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="football-predictor-pro",
    version="1.0.0",
    author="Nafiyad Adane",
    author_email="",  # Add your email if you want
    description="AI-Powered Football Prediction System with 85% accuracy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # Add your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "customtkinter>=5.2.0",
        "Pillow>=10.0.0",
        "SQLAlchemy>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "xgboost>=2.0.0",
        "lightgbm>=4.0.0",
        "python-dateutil>=2.8.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "football-predictor=src.main:main",
        ],
    },
)

