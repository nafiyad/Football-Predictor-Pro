"""Application configuration."""
import os


class Config:
    """Application configuration class."""
    
    # Application
    APP_NAME = "Football Predictor Pro"
    APP_VERSION = "1.0.0"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    SEED_DIR = os.path.join(DATA_DIR, 'seed')
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    ML_MODELS_DIR = os.path.join(BASE_DIR, 'src', 'ml', 'saved_models')
    
    # Database
    DB_PATH = os.path.join(BASE_DIR, 'src', 'database', 'predictions.db')
    
    # ML Model Settings
    MODEL_VERSION = "1.0"
    ENSEMBLE_WEIGHTS = {
        'xgboost': 0.35,
        'lightgbm': 0.35,
        'random_forest': 0.30
    }
    
    # Feature Engineering
    FORM_WINDOW = 10  # Last N matches for form calculation
    H2H_WINDOW = 5    # Last N head-to-head matches
    
    # UI Settings
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    MIN_WIDTH = 1200
    MIN_HEIGHT = 700
    
    # Theme
    DEFAULT_THEME = "dark"  # "dark" or "light"
    COLOR_THEME = "blue"    # "blue", "green", "dark-blue"
    
    # Prediction Confidence Thresholds
    HIGH_CONFIDENCE = 0.70
    MEDIUM_CONFIDENCE = 0.55
    LOW_CONFIDENCE = 0.40
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        directories = [
            cls.DATA_DIR,
            cls.SEED_DIR,
            cls.ASSETS_DIR,
            cls.ML_MODELS_DIR,
            os.path.dirname(cls.DB_PATH)
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)



