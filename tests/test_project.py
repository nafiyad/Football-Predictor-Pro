"""Tests for Football Predictor Pro - basic import and unit tests."""
import os
import sys

# Verify project structure
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
sys.path.insert(0, SRC_DIR)


def test_src_directory_exists():
    """Test that src directory exists."""
    assert os.path.isdir(SRC_DIR)


def test_services_directory_exists():
    """Test that services directory exists."""
    services_dir = os.path.join(SRC_DIR, 'services')
    assert os.path.isdir(services_dir)


def test_ml_directory_exists():
    """Test that ml directory exists."""
    ml_dir = os.path.join(SRC_DIR, 'ml')
    assert os.path.isdir(ml_dir)


def test_feature_engineering_file_exists():
    """Test feature engineering file exists."""
    fe_file = os.path.join(SRC_DIR, 'services', 'feature_engineering.py')
    assert os.path.isfile(fe_file)


def test_prediction_service_file_exists():
    """Test prediction service file exists."""
    ps_file = os.path.join(SRC_DIR, 'services', 'prediction_service.py')
    assert os.path.isfile(ps_file)


def test_data_service_file_exists():
    """Test data service file exists."""
    ds_file = os.path.join(SRC_DIR, 'services', 'data_service.py')
    assert os.path.isfile(ds_file)


def test_bet_calculator_file_exists():
    """Test bet calculator file exists."""
    bc_file = os.path.join(SRC_DIR, 'services', 'bet_calculator.py')
    assert os.path.isfile(bc_file)


def test_advanced_models_file_exists():
    """Test advanced models file exists."""
    am_file = os.path.join(SRC_DIR, 'ml', 'advanced_models.py')
    assert os.path.isfile(am_file)


def test_web_app_exists():
    """Test web app file exists."""
    web_file = os.path.join(PROJECT_ROOT, 'web_app.py')
    assert os.path.isfile(web_file)


def test_dockerfile_exists():
    """Test Dockerfile exists."""
    df_file = os.path.join(PROJECT_ROOT, 'Dockerfile')
    assert os.path.isfile(df_file)


def test_github_workflow_exists():
    """Test GitHub workflow exists."""
    wf_dir = os.path.join(PROJECT_ROOT, '.github', 'workflows')
    assert os.path.isdir(wf_dir)