"""Bet Value Calculator Service.

Calculates expected value (EV) based on model predictions and bookmaker odds.
"""
import numpy as np
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class BetRecommendation:
    """Bet recommendation with full analysis."""
    market: str
    selection: str
    probability: float
    bookmaker_odds: float
    fair_odds: float
    expected_value: float
    stake_percentage: float
    confidence: str
    rationale: str


class BetValueCalculator:
    """Calculate bet expected value from predictions."""
    
    KELLY_MULTIPLIER = 0.25
    HIGH_EV_THRESHOLD = 0.10
    MEDIUM_EV_THRESHOLD = 0.05
    LOW_EV_THRESHOLD = 0.02
    
    def calculate_ev(self, prediction_probability: float, bookmaker_odds: float, include_commission: float = 0.0) -> Dict[str, float]:
        """Calculate expected value for a bet."""
        fair_odds = 1.0 / prediction_probability if prediction_probability > 0 else float('inf')
        net_odds = bookmaker_odds * (1 - include_commission)
        ev = prediction_probability * net_odds - 1
        edge = (fair_odds / bookmaker_odds - 1) if bookmaker_odds > 0 else 0
        
        return {
            'prediction_probability': prediction_probability,
            'bookmaker_odds': bookmaker_odds,
            'fair_odds': fair_odds,
            'net_odds': net_odds,
            'expected_value': ev,
            'ev_percentage': ev,
            'edge_over_fair': edge
        }
    
    def calculate_kelly_stake(self, ev: float, bankroll: float, multiplier: float = None) -> float:
        """Calculate Kelly Criterion stake."""
        if ev <= 0:
            return 0
        kelly_stake = 2 * ev * (multiplier or self.KELLY_MULTIPLIER)
        return min(kelly_stake, 0.20) * bankroll
    
    def analyze_prediction(self, prediction, odds_home: float, odds_draw: float, odds_away: float, bankroll: float = 1000.0) -> List[BetRecommendation]:
        """Analyze a prediction for betting opportunities."""
        recommendations = []
        markets = [
            ('Home', prediction.home_win_prob, odds_home),
            ('Draw', prediction.draw_prob, odds_draw),
            ('Away', prediction.away_win_prob, odds_away),
        ]
        
        for selection, prob, odds in markets:
            calc = self.calculate_ev(prob, odds)
            if calc['expected_value'] <= 0:
                continue
            
            stake = self.calculate_kelly_stake(calc['expected_value'], bankroll)
            
            if calc['ev_percentage'] >= self.HIGH_EV_THRESHOLD:
                confidence = 'high'
            elif calc['ev_percentage'] >= self.MEDIUM_EV_THRESHOLD:
                confidence = 'medium'
            elif calc['ev_percentage'] >= self.LOW_EV_THRESHOLD:
                confidence = 'low'
            else:
                confidence = 'none'
            
            recommendations.append(BetRecommendation(
                market='1X2',
                selection=selection,
                probability=prob,
                bookmaker_odds=odds,
                fair_odds=calc['fair_odds'],
                expected_value=calc['expected_value'],
                stake_percentage=stake / bankroll,
                confidence=confidence,
                rationale=f"EV: {calc['ev_percentage']:.1%}"
            ))
        
        return sorted(recommendations, key=lambda x: x.expected_value, reverse=True)