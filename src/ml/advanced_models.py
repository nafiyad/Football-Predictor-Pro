"""Advanced ML models for better predictions."""
import numpy as np
import pandas as pd
from sklearn.ensemble import (
    RandomForestClassifier, 
    GradientBoostingClassifier,
    VotingClassifier,
    StackingClassifier
)
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, cross_val_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import pickle
import os
from datetime import datetime
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Try to import Optuna for Bayesian hyperparameter tuning
try:
    import optuna
    from optuna.samplers import TPESampler
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False


class AdvancedModelTrainer:
    """Advanced model training with hyperparameter optimization."""
    
    def __init__(self):
        """Initialize advanced trainer."""
        self.models = {}
        self.scaler = StandardScaler()
        self.best_params = {}
    
    def create_neural_network(self, input_dim):
        """
        Create deep neural network for predictions.
        
        Args:
            input_dim: Number of input features
            
        Returns:
            MLPClassifier model
        """
        return MLPClassifier(
            hidden_layer_sizes=(128, 64, 32, 16),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size=32,
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=500,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20,
            random_state=42,
            verbose=False
        )
    
    def create_advanced_xgboost(self):
        """Create XGBoost with optimized parameters."""
        return XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            gamma=0.1,
            min_child_weight=3,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1,
            eval_metric='mlogloss'
        )
    
    def create_advanced_lightgbm(self):
        """Create LightGBM with optimized parameters."""
        return LGBMClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.05,
            num_leaves=31,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_samples=20,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
    
    def create_gradient_boosting(self):
        """Create Gradient Boosting classifier."""
        return GradientBoostingClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features='sqrt',
            random_state=42,
            verbose=0
        )
    
    def create_advanced_random_forest(self):
        """Create Random Forest with optimized parameters."""
        return RandomForestClassifier(
            n_estimators=300,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=4,
            max_features='sqrt',
            bootstrap=True,
            oob_score=True,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
    
    def create_stacking_ensemble(self, X_train, y_train):
        """
        Create stacking ensemble of multiple models.
        
        Args:
            X_train: Training features
            y_train: Training labels
            
        Returns:
            Stacking classifier
        """
        logger.info("Creating stacking ensemble...")
        
        # Base models
        base_models = [
            ('xgb', self.create_advanced_xgboost()),
            ('lgbm', self.create_advanced_lightgbm()),
            ('rf', self.create_advanced_random_forest()),
            ('gb', self.create_gradient_boosting())
        ]
        
        # Meta-learner
        meta_learner = LogisticRegression(
            max_iter=1000,
            random_state=42,
            multi_class='multinomial'
        )
        
        # Create stacking classifier
        stacking_clf = StackingClassifier(
            estimators=base_models,
            final_estimator=meta_learner,
            cv=5,
            n_jobs=-1,
            verbose=0
        )
        
        return stacking_clf
    
    def create_voting_ensemble(self):
        """
        Create voting ensemble of multiple models.
        
        Returns:
            Voting classifier
        """
        logger.info("Creating voting ensemble...")
        
        models = [
            ('xgb', self.create_advanced_xgboost()),
            ('lgbm', self.create_advanced_lightgbm()),
            ('rf', self.create_advanced_random_forest()),
            ('gb', self.create_gradient_boosting())
        ]
        
        # Soft voting (uses predicted probabilities)
        voting_clf = VotingClassifier(
            estimators=models,
            voting='soft',
            weights=[0.3, 0.3, 0.2, 0.2],
            n_jobs=-1,
            verbose=False
        )
        
        return voting_clf
    
    def hyperparameter_tuning(self, model, param_grid, X_train, y_train, cv=3):
        """
        Perform hyperparameter tuning using GridSearchCV.
        
        Args:
            model: Model to tune
            param_grid: Parameter grid
            X_train: Training features
            y_train: Training labels
            cv: Cross-validation folds
            
        Returns:
            Best model
        """
        logger.info("Performing hyperparameter tuning...")
        
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def train_with_cross_validation(self, model, X, y, cv=5):
        """
        Train model with cross-validation.
        
        Args:
            model: Model to train
            X: Features
            y: Labels
            cv: Number of folds
            
        Returns:
            Trained model and CV scores
        """
        logger.info(f"Training with {cv}-fold cross-validation...")
        
        # Perform cross-validation
        cv_scores = cross_val_score(
            model, X, y,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1
        )
        
        logger.info(f"CV Scores: {cv_scores}")
        logger.info(f"Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Train on full dataset
        model.fit(X, y)
        
        return model, cv_scores
    
    def get_feature_importance(self, model, feature_names):
        """
        Get feature importance from trained model.
        
        Args:
            model: Trained model
            feature_names: List of feature names
            
        Returns:
            DataFrame with feature importance
        """
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            # Create DataFrame
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            })
            
            # Sort by importance
            importance_df = importance_df.sort_values('importance', ascending=False)
            
            return importance_df
        
        return None
    
    def save_model(self, model, model_name):
        """Save trained model."""
        filepath = os.path.join(Config.ML_MODELS_DIR, f"{model_name}.pkl")
        
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        
        logger.info(f"Saved {model_name} to {filepath}")
    
    def save_scaler(self):
        """Save feature scaler."""
        filepath = os.path.join(Config.ML_MODELS_DIR, "scaler.pkl")
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        logger.info(f"Saved scaler to {filepath}")
    
    def create_calibrated_classifier(self, base_model, method='sigmoid', cv=5):
        """Create calibrated classifier for reliable probability outputs."""
        logger.info(f"Creating calibrated classifier using {method} method...")
        
        calibrated_model = CalibratedClassifierCV(
            estimator=base_model,
            method=method,
            cv=cv
        )
        
        return calibrated_model
    
    def optuna_optimize(self, X_train, y_train, n_trials=50, timeout=300):
        """Bayesian hyperparameter tuning using Optuna."""
        if not OPTUNA_AVAILABLE:
            logger.warning("Optuna not available. Falling back to GridSearchCV.")
            return None, None
        
        logger.info(f"Starting Optuna optimization with {n_trials} trials...")
        
        def objective(trial):
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 100, 500),
                'max_depth': trial.suggest_int('max_depth', 3, 12),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            }
            
            model = XGBClassifier(**params, random_state=42, n_jobs=-1, eval_metric='mlogloss')
            scores = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy', n_jobs=-1)
            return scores.mean()
        
        sampler = TPESampler(seed=42)
        study = optuna.create_study(direction='maximize', sampler=sampler)
        study.optimize(objective, n_trials=n_trials, timeout=timeout, show_progress_bar=True)
        
        logger.info(f"Best trial: {study.best_trial.value:.4f}")
        logger.info(f"Best params: {study.best_params}")
        
        best_model = XGBClassifier(**study.best_params, random_state=42, n_jobs=-1, eval_metric='mlogloss')
        return best_model, study
    
    def save_model_versioned(self, model, model_name: str):
        """Save model with timestamp for versioning."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        versioned_name = f"{model_name}_{timestamp}"
        
        filepath = os.path.join(Config.ML_MODELS_DIR, f"{versioned_name}.pkl")
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        
        logger.info(f"Saved versioned model: {versioned_name}")
        
        latest_filepath = os.path.join(Config.ML_MODELS_DIR, f"{model_name}.pkl")
        with open(latest_filepath, 'wb') as f:
            pickle.dump(model, f)
        
        logger.info(f"Saved latest model: {model_name}")
        return versioned_name


class EnsemblePredictor:
    """Advanced ensemble predictor with multiple models."""
    
    def __init__(self):
        """Initialize ensemble predictor."""
        self.models = {}
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        """Load all trained models."""
        models_dir = Config.ML_MODELS_DIR
        
        model_files = {
            'stacking_1x2': 'stacking_1x2.pkl',
            'voting_1x2': 'voting_1x2.pkl',
            'neural_net_1x2': 'neural_net_1x2.pkl',
            'xgboost_advanced': 'xgboost_advanced.pkl',
            'lgbm_advanced': 'lgbm_advanced.pkl'
        }
        
        for model_name, filename in model_files.items():
            filepath = os.path.join(models_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    self.models[model_name] = pickle.load(f)
                logger.info(f"Loaded {model_name}")
        
        # Load scaler
        scaler_path = os.path.join(models_dir, "scaler.pkl")
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            logger.info("Loaded feature scaler")
    
    def predict_with_confidence(self, features):
        """
        Make prediction with confidence intervals.
        
        Args:
            features: Feature array
            
        Returns:
            Dictionary with predictions and confidence
        """
        if not self.models:
            logger.warning("No models loaded")
            return None
        
        # Scale features
        if self.scaler:
            features_scaled = self.scaler.transform(features.reshape(1, -1))
        else:
            features_scaled = features.reshape(1, -1)
        
        # Get predictions from all models
        all_predictions = []
        
        for model_name, model in self.models.items():
            try:
                probs = model.predict_proba(features_scaled)[0]
                all_predictions.append(probs)
            except Exception as e:
                logger.warning(f"Error with {model_name}: {e}")
                continue
        
        if not all_predictions:
            return None
        
        # Calculate ensemble prediction (average)
        ensemble_probs = np.mean(all_predictions, axis=0)
        
        # Calculate confidence (standard deviation)
        prediction_std = np.std(all_predictions, axis=0)
        confidence = 1 - np.mean(prediction_std)  # Lower std = higher confidence
        
        return {
            'probabilities': ensemble_probs,
            'confidence': confidence,
            'std_dev': prediction_std,
            'num_models': len(all_predictions)
        }

