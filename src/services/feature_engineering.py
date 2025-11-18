"""Feature engineering for ML models."""
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from models.database import Match, MatchStats, Team
from database.connection import get_session
from utils.config import Config


class FeatureEngineer:
    """Feature engineering service for match predictions."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize feature engineer."""
        self.session = session or get_session()
        self.form_window = Config.FORM_WINDOW
        self.h2h_window = Config.H2H_WINDOW
    
    def engineer_match_features(self, match_id: int) -> np.ndarray:
        """
        Engineer features for a specific match.
        
        Args:
            match_id: Match ID
            
        Returns:
            Feature array
        """
        match = self.session.query(Match).filter_by(id=match_id).first()
        
        if not match:
            raise ValueError(f"Match {match_id} not found")
        
        # Get team features
        home_features = self.get_team_features(match.home_team_id, venue='home', before_date=match.date)
        away_features = self.get_team_features(match.away_team_id, venue='away', before_date=match.date)
        
        # Get head-to-head features
        h2h_features = self.get_h2h_features(match.home_team_id, match.away_team_id, before_date=match.date)
        
        # Combine all features
        features = np.concatenate([home_features, away_features, h2h_features])
        
        return features
    
    def get_team_features(
        self,
        team_id: int,
        venue: str = 'all',
        before_date: Optional[datetime] = None,
        last_n: int = None
    ) -> np.ndarray:
        """
        Calculate team form features.
        
        Args:
            team_id: Team ID
            venue: 'home', 'away', or 'all'
            before_date: Only consider matches before this date
            last_n: Number of recent matches to consider
            
        Returns:
            Feature array
        """
        if last_n is None:
            last_n = self.form_window
        
        if before_date is None:
            before_date = datetime.now()
        
        # Build query
        query = self.session.query(Match).filter(
            Match.status == 'finished',
            Match.date < before_date
        )
        
        if venue == 'home':
            query = query.filter(Match.home_team_id == team_id)
        elif venue == 'away':
            query = query.filter(Match.away_team_id == team_id)
        else:
            query = query.filter(
                (Match.home_team_id == team_id) | (Match.away_team_id == team_id)
            )
        
        matches = query.order_by(Match.date.desc()).limit(last_n).all()
        
        if not matches:
            # Return zeros if no matches found
            return np.zeros(10)
        
        # Calculate statistics
        goals_scored = []
        goals_conceded = []
        points = []
        xg_for = []
        xg_against = []
        
        for match in matches:
            is_home = match.home_team_id == team_id
            
            if is_home:
                goals_scored.append(match.home_goals)
                goals_conceded.append(match.away_goals)
                
                if match.home_goals > match.away_goals:
                    points.append(3)
                elif match.home_goals == match.away_goals:
                    points.append(1)
                else:
                    points.append(0)
            else:
                goals_scored.append(match.away_goals)
                goals_conceded.append(match.home_goals)
                
                if match.away_goals > match.home_goals:
                    points.append(3)
                elif match.away_goals == match.home_goals:
                    points.append(1)
                else:
                    points.append(0)
            
            # Get xG stats if available
            stats = self.session.query(MatchStats).filter_by(
                match_id=match.id,
                team_id=team_id
            ).first()
            
            if stats and stats.xg:
                xg_for.append(stats.xg)
                
                # Get opponent xG
                opponent_id = match.away_team_id if is_home else match.home_team_id
                opp_stats = self.session.query(MatchStats).filter_by(
                    match_id=match.id,
                    team_id=opponent_id
                ).first()
                
                if opp_stats and opp_stats.xg:
                    xg_against.append(opp_stats.xg)
        
        # Calculate features
        features = [
            np.mean(goals_scored) if goals_scored else 0,  # Avg goals scored
            np.mean(goals_conceded) if goals_conceded else 0,  # Avg goals conceded
            np.mean(points) if points else 0,  # Avg points per game
            sum(1 for p in points if p == 3) / len(points) if points else 0,  # Win rate
            sum(1 for p in points if p == 1) / len(points) if points else 0,  # Draw rate
            sum(1 for g in goals_scored if g == 0) / len(goals_scored) if goals_scored else 0,  # Failed to score rate
            sum(1 for g in goals_conceded if g == 0) / len(goals_conceded) if goals_conceded else 0,  # Clean sheet rate
            np.mean(xg_for) if xg_for else np.mean(goals_scored) if goals_scored else 0,  # Avg xG for
            np.mean(xg_against) if xg_against else np.mean(goals_conceded) if goals_conceded else 0,  # Avg xG against
            len(matches) / last_n  # Data completeness ratio
        ]
        
        return np.array(features)
    
    def get_h2h_features(
        self,
        home_team_id: int,
        away_team_id: int,
        before_date: Optional[datetime] = None,
        last_n: int = None
    ) -> np.ndarray:
        """
        Calculate head-to-head features.
        
        Args:
            home_team_id: Home team ID
            away_team_id: Away team ID
            before_date: Only consider matches before this date
            last_n: Number of recent H2H matches to consider
            
        Returns:
            Feature array
        """
        if last_n is None:
            last_n = self.h2h_window
        
        if before_date is None:
            before_date = datetime.now()
        
        # Get head-to-head matches
        h2h_matches = self.session.query(Match).filter(
            (
                (Match.home_team_id == home_team_id) & (Match.away_team_id == away_team_id)
            ) | (
                (Match.home_team_id == away_team_id) & (Match.away_team_id == home_team_id)
            ),
            Match.status == 'finished',
            Match.date < before_date
        ).order_by(Match.date.desc()).limit(last_n).all()
        
        if not h2h_matches:
            return np.zeros(5)
        
        # Calculate H2H statistics
        home_wins = 0
        away_wins = 0
        draws = 0
        total_goals_home = 0
        total_goals_away = 0
        
        for match in h2h_matches:
            if match.home_team_id == home_team_id:
                total_goals_home += match.home_goals
                total_goals_away += match.away_goals
                
                if match.home_goals > match.away_goals:
                    home_wins += 1
                elif match.home_goals < match.away_goals:
                    away_wins += 1
                else:
                    draws += 1
            else:
                total_goals_home += match.away_goals
                total_goals_away += match.home_goals
                
                if match.away_goals > match.home_goals:
                    home_wins += 1
                elif match.away_goals < match.home_goals:
                    away_wins += 1
                else:
                    draws += 1
        
        num_matches = len(h2h_matches)
        
        features = [
            home_wins / num_matches,  # Home team win rate in H2H
            draws / num_matches,  # Draw rate in H2H
            away_wins / num_matches,  # Away team win rate in H2H
            total_goals_home / num_matches,  # Avg goals for home team in H2H
            total_goals_away / num_matches  # Avg goals for away team in H2H
        ]
        
        return np.array(features)
    
    def get_feature_names(self) -> List[str]:
        """Get feature names for model interpretation."""
        home_features = [
            'home_avg_goals_scored',
            'home_avg_goals_conceded',
            'home_avg_points',
            'home_win_rate',
            'home_draw_rate',
            'home_failed_to_score_rate',
            'home_clean_sheet_rate',
            'home_avg_xg_for',
            'home_avg_xg_against',
            'home_data_completeness'
        ]
        
        away_features = [
            'away_avg_goals_scored',
            'away_avg_goals_conceded',
            'away_avg_points',
            'away_win_rate',
            'away_draw_rate',
            'away_failed_to_score_rate',
            'away_clean_sheet_rate',
            'away_avg_xg_for',
            'away_avg_xg_against',
            'away_data_completeness'
        ]
        
        h2h_features = [
            'h2h_home_win_rate',
            'h2h_draw_rate',
            'h2h_away_win_rate',
            'h2h_avg_goals_home',
            'h2h_avg_goals_away'
        ]
        
        return home_features + away_features + h2h_features



