"""Prediction service with ensemble ML models."""
import os
import pickle
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Tuple
from sqlalchemy.orm import Session
from models.database import Prediction, Match
from database.connection import get_session
from services.feature_engineering import FeatureEngineer
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PredictionService:
    """Service for making match predictions using ensemble ML models."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize prediction service."""
        self.session = session or get_session()
        self.feature_engineer = FeatureEngineer(self.session)
        self.models_loaded = False
        self.models = {}
        
        # Try to load models
        try:
            self.load_models()
        except Exception as e:
            logger.warning(f"Could not load ML models: {e}")
            logger.info("Models will need to be trained first.")
    
    def load_models(self):
        """Load trained ML models."""
        models_dir = Config.ML_MODELS_DIR
        
        model_files = {
            'xgboost_1x2': 'xgboost_1x2.pkl',
            'lgbm_1x2': 'lgbm_1x2.pkl',
            'rf_1x2': 'rf_1x2.pkl',
            'xgboost_btts': 'xgboost_btts.pkl',
            'rf_ou25': 'rf_ou25.pkl'
        }
        
        for model_name, filename in model_files.items():
            filepath = os.path.join(models_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    self.models[model_name] = pickle.load(f)
                logger.info(f"Loaded model: {model_name}")
            else:
                logger.warning(f"Model file not found: {filepath}")
        
        if len(self.models) > 0:
            self.models_loaded = True
            logger.info(f"Successfully loaded {len(self.models)} models")
        else:
            logger.warning("No models loaded. Please train models first.")
    
    def get_match_prediction(self, match_id: int, force_refresh: bool = False) -> Optional[Prediction]:
        """
        Get prediction for a match.
        
        Args:
            match_id: Match ID
            force_refresh: Force regenerate prediction even if exists
            
        Returns:
            Prediction object or None
        """
        # Check if prediction already exists
        if not force_refresh:
            existing = self.session.query(Prediction).filter_by(match_id=match_id).first()
            if existing:
                return existing
        
        # Check if models are loaded
        if not self.models_loaded:
            logger.error("Models not loaded. Cannot generate prediction.")
            return self._create_dummy_prediction(match_id)
        
        try:
            # Generate features
            features = self.feature_engineer.engineer_match_features(match_id)
            
            # Get predictions from each model
            predictions = self._ensemble_predict(features)
            
            # Create prediction object
            prediction = Prediction(
                match_id=match_id,
                prediction_date=datetime.now(),
                home_win_prob=float(predictions['home_win_prob']),
                draw_prob=float(predictions['draw_prob']),
                away_win_prob=float(predictions['away_win_prob']),
                btts_prob=float(predictions.get('btts_prob', 0.5)),
                over_2_5_prob=float(predictions.get('over_2_5_prob', 0.5)),
                under_2_5_prob=float(predictions.get('under_2_5_prob', 0.5)),
                predicted_home_goals=float(predictions.get('predicted_home_goals', 1.5)),
                predicted_away_goals=float(predictions.get('predicted_away_goals', 1.2)),
                confidence=float(predictions['confidence']),
                model_version=Config.MODEL_VERSION
            )
            
            # Save prediction
            self.session.add(prediction)
            self.session.commit()
            
            logger.info(f"Generated prediction for match {match_id}")
            return prediction
            
        except Exception as e:
            logger.error(f"Error generating prediction for match {match_id}: {e}")
            return self._create_dummy_prediction(match_id)
    
    def _ensemble_predict(self, features: np.ndarray) -> Dict:
        """
        Make ensemble prediction using multiple models.
        
        Args:
            features: Feature array
            
        Returns:
            Dictionary with prediction results
        """
        features_2d = features.reshape(1, -1)
        
        # Get 1X2 predictions from multiple models
        predictions_1x2 = []
        weights = []
        
        if 'xgboost_1x2' in self.models:
            pred = self.models['xgboost_1x2'].predict_proba(features_2d)[0]
            predictions_1x2.append(pred)
            weights.append(Config.ENSEMBLE_WEIGHTS['xgboost'])
        
        if 'lgbm_1x2' in self.models:
            pred = self.models['lgbm_1x2'].predict_proba(features_2d)[0]
            predictions_1x2.append(pred)
            weights.append(Config.ENSEMBLE_WEIGHTS['lightgbm'])
        
        if 'rf_1x2' in self.models:
            pred = self.models['rf_1x2'].predict_proba(features_2d)[0]
            predictions_1x2.append(pred)
            weights.append(Config.ENSEMBLE_WEIGHTS['random_forest'])
        
        # Weighted average of predictions
        if predictions_1x2:
            weights = np.array(weights) / sum(weights)  # Normalize weights
            ensemble_probs = np.average(predictions_1x2, axis=0, weights=weights)
        else:
            # Fallback to uniform distribution
            ensemble_probs = np.array([0.33, 0.33, 0.34])
        
        # Ensure probabilities sum to 1
        ensemble_probs = ensemble_probs / ensemble_probs.sum()
        
        # Calculate confidence (max probability)
        confidence = float(np.max(ensemble_probs))
        
        # BTTS prediction
        btts_prob = 0.5
        if 'xgboost_btts' in self.models:
            try:
                btts_prob = self.models['xgboost_btts'].predict_proba(features_2d)[0][1]
            except:
                pass
        
        # Over/Under 2.5 prediction
        over_2_5_prob = 0.5
        under_2_5_prob = 0.5
        if 'rf_ou25' in self.models:
            try:
                over_2_5_prob = self.models['rf_ou25'].predict_proba(features_2d)[0][1]
                under_2_5_prob = 1 - over_2_5_prob
            except:
                pass
        
        # Estimate goal predictions based on features
        # Use team averages from features
        home_avg_goals = features[0] if len(features) > 0 else 1.5
        away_avg_goals = features[10] if len(features) > 10 else 1.2
        
        return {
            'home_win_prob': ensemble_probs[0],
            'draw_prob': ensemble_probs[1],
            'away_win_prob': ensemble_probs[2],
            'btts_prob': btts_prob,
            'over_2_5_prob': over_2_5_prob,
            'under_2_5_prob': under_2_5_prob,
            'predicted_home_goals': home_avg_goals,
            'predicted_away_goals': away_avg_goals,
            'confidence': confidence
        }
    
    def _create_dummy_prediction(self, match_id: int) -> Prediction:
        """
        Create a dummy prediction when models are not available.
        
        Args:
            match_id: Match ID
            
        Returns:
            Dummy prediction
        """
        # Check if already exists
        existing = self.session.query(Prediction).filter_by(match_id=match_id).first()
        if existing:
            return existing
        
        # Create basic prediction based on simple heuristics
        match = self.session.query(Match).filter_by(id=match_id).first()
        
        if not match:
            return None
        
        # Simple heuristic: slight home advantage
        prediction = Prediction(
            match_id=match_id,
            prediction_date=datetime.now(),
            home_win_prob=0.40,
            draw_prob=0.30,
            away_win_prob=0.30,
            btts_prob=0.50,
            over_2_5_prob=0.50,
            under_2_5_prob=0.50,
            predicted_home_goals=1.5,
            predicted_away_goals=1.2,
            confidence=0.40,
            model_version="dummy"
        )
        
        self.session.add(prediction)
        self.session.commit()
        
        return prediction
    
    def get_recommended_bet(self, prediction: Prediction) -> Optional[Dict]:
        """
        Get recommended bet based on prediction.
        
        Args:
            prediction: Prediction object
            
        Returns:
            Dictionary with bet recommendation or None
        """
        if prediction.confidence < Config.LOW_CONFIDENCE:
            return None
        
        # Find the highest probability outcome
        outcomes = {
            'Home Win': prediction.home_win_prob,
            'Draw': prediction.draw_prob,
            'Away Win': prediction.away_win_prob
        }
        
        best_outcome = max(outcomes, key=outcomes.get)
        best_prob = outcomes[best_outcome]
        
        if best_prob >= Config.MEDIUM_CONFIDENCE:
            return {
                'market': '1X2',
                'selection': best_outcome,
                'probability': best_prob,
                'confidence': prediction.confidence,
                'suggested_odds': round(1 / best_prob, 2)
            }
        
        # Check BTTS
        if prediction.btts_prob >= Config.MEDIUM_CONFIDENCE:
            return {
                'market': 'BTTS',
                'selection': 'Yes',
                'probability': prediction.btts_prob,
                'confidence': prediction.confidence,
                'suggested_odds': round(1 / prediction.btts_prob, 2)
            }
        
        # Check Over/Under
        if prediction.over_2_5_prob >= Config.MEDIUM_CONFIDENCE:
            return {
                'market': 'Over/Under 2.5',
                'selection': 'Over 2.5',
                'probability': prediction.over_2_5_prob,
                'confidence': prediction.confidence,
                'suggested_odds': round(1 / prediction.over_2_5_prob, 2)
            }
        
        return None



