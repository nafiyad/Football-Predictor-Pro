"""Backtesting service for model evaluation."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.database import Match, Prediction
from database.connection import get_session
from services.prediction_service import PredictionService
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BacktestService:
    """Service for backtesting predictions."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize backtest service."""
        self.session = session or get_session()
        self.prediction_service = PredictionService(self.session)
    
    def backtest_predictions(
        self,
        start_date: datetime,
        end_date: datetime,
        league_id: Optional[int] = None
    ) -> Dict:
        """
        Backtest predictions for a date range.
        
        Args:
            start_date: Start date for backtest
            end_date: End date for backtest
            league_id: Optional league filter
            
        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Starting backtest from {start_date} to {end_date}")
        
        # Get finished matches in date range
        query = self.session.query(Match).filter(
            Match.status == 'finished',
            Match.date >= start_date,
            Match.date <= end_date
        )
        
        if league_id:
            query = query.filter(Match.league_id == league_id)
        
        matches = query.all()
        
        if not matches:
            return {
                'total_matches': 0,
                'accuracy': 0,
                'message': 'No matches found in date range'
            }
        
        logger.info(f"Backtesting {len(matches)} matches")
        
        results = {
            'total_matches': len(matches),
            'correct_predictions': 0,
            'incorrect_predictions': 0,
            'accuracy': 0,
            'by_confidence': {
                'high': {'correct': 0, 'total': 0},
                'medium': {'correct': 0, 'total': 0},
                'low': {'correct': 0, 'total': 0}
            },
            'by_outcome': {
                'home_win': {'correct': 0, 'total': 0},
                'draw': {'correct': 0, 'total': 0},
                'away_win': {'correct': 0, 'total': 0}
            },
            'roi_simulation': 0,
            'details': []
        }
        
        total_stake = 0
        total_return = 0
        
        for match in matches:
            # Get or generate prediction
            prediction = self.session.query(Prediction).filter_by(match_id=match.id).first()
            
            if not prediction:
                # Generate prediction for backtest
                try:
                    prediction = self.prediction_service.get_match_prediction(match.id)
                except Exception as e:
                    logger.warning(f"Could not generate prediction for match {match.id}: {e}")
                    continue
            
            if not prediction:
                continue
            
            # Determine predicted outcome
            probs = {
                'home': prediction.home_win_prob,
                'draw': prediction.draw_prob,
                'away': prediction.away_win_prob
            }
            predicted_outcome = max(probs, key=probs.get)
            predicted_prob = probs[predicted_outcome]
            
            # Determine actual outcome
            if match.home_goals > match.away_goals:
                actual_outcome = 'home'
            elif match.home_goals < match.away_goals:
                actual_outcome = 'away'
            else:
                actual_outcome = 'draw'
            
            # Check if prediction was correct
            is_correct = (predicted_outcome == actual_outcome)
            
            if is_correct:
                results['correct_predictions'] += 1
            else:
                results['incorrect_predictions'] += 1
            
            # Track by confidence level
            if prediction.confidence >= 0.70:
                conf_level = 'high'
            elif prediction.confidence >= 0.55:
                conf_level = 'medium'
            else:
                conf_level = 'low'
            
            results['by_confidence'][conf_level]['total'] += 1
            if is_correct:
                results['by_confidence'][conf_level]['correct'] += 1
            
            # Track by outcome type
            results['by_outcome'][f'{actual_outcome}_win' if actual_outcome != 'draw' else 'draw']['total'] += 1
            if is_correct:
                results['by_outcome'][f'{actual_outcome}_win' if actual_outcome != 'draw' else 'draw']['correct'] += 1
            
            # Simulate betting (flat stake)
            stake = 10  # $10 flat stake
            odds = 1 / predicted_prob  # Implied odds
            
            total_stake += stake
            if is_correct:
                total_return += stake * odds
            
            # Store details
            results['details'].append({
                'match_id': match.id,
                'date': match.date,
                'home_team': match.home_team.name,
                'away_team': match.away_team.name,
                'score': f"{match.home_goals}-{match.away_goals}",
                'predicted': predicted_outcome,
                'actual': actual_outcome,
                'correct': is_correct,
                'confidence': prediction.confidence
            })
        
        # Calculate overall accuracy
        total_predictions = results['correct_predictions'] + results['incorrect_predictions']
        results['accuracy'] = (results['correct_predictions'] / total_predictions * 100) if total_predictions > 0 else 0
        
        # Calculate ROI
        results['roi_simulation'] = ((total_return - total_stake) / total_stake * 100) if total_stake > 0 else 0
        results['total_stake'] = total_stake
        results['total_return'] = total_return
        results['profit'] = total_return - total_stake
        
        # Calculate accuracy by confidence
        for level in results['by_confidence']:
            total = results['by_confidence'][level]['total']
            correct = results['by_confidence'][level]['correct']
            results['by_confidence'][level]['accuracy'] = (correct / total * 100) if total > 0 else 0
        
        # Calculate accuracy by outcome
        for outcome in results['by_outcome']:
            total = results['by_outcome'][outcome]['total']
            correct = results['by_outcome'][outcome]['correct']
            results['by_outcome'][outcome]['accuracy'] = (correct / total * 100) if total > 0 else 0
        
        logger.info(f"Backtest completed: {results['accuracy']:.1f}% accuracy")
        
        return results
    
    def get_model_performance_history(self, days: int = 30) -> List[Dict]:
        """
        Get model performance over time.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            List of daily performance metrics
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        daily_performance = []
        
        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)
            
            # Backtest for this day
            day_results = self.backtest_predictions(current_date, next_date)
            
            if day_results['total_matches'] > 0:
                daily_performance.append({
                    'date': current_date,
                    'matches': day_results['total_matches'],
                    'accuracy': day_results['accuracy'],
                    'roi': day_results.get('roi_simulation', 0)
                })
            
            current_date = next_date
        
        return daily_performance
    
    def compare_models(self, match_ids: List[int]) -> Dict:
        """
        Compare performance of different models.
        
        Args:
            match_ids: List of match IDs to compare
            
        Returns:
            Comparison results
        """
        # This would compare individual model predictions
        # For now, we'll return a placeholder
        return {
            'message': 'Model comparison feature coming soon',
            'models': ['XGBoost', 'LightGBM', 'Random Forest']
        }



