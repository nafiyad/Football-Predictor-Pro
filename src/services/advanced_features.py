"""Advanced feature engineering for better predictions."""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from models.database import Match, MatchStats, Team
from database.connection import get_session
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AdvancedFeatureEngineer:
    """Advanced feature engineering with sophisticated statistics."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize advanced feature engineer."""
        self.session = session or get_session()
    
    def engineer_advanced_features(self, match_id: int) -> np.ndarray:
        """
        Engineer comprehensive advanced features.
        
        Args:
            match_id: Match ID
            
        Returns:
            Advanced feature array
        """
        match = self.session.query(Match).filter_by(id=match_id).first()
        
        if not match:
            raise ValueError(f"Match {match_id} not found")
        
        # Basic features
        home_basic = self.get_basic_features(match.home_team_id, 'home', match.date)
        away_basic = self.get_basic_features(match.away_team_id, 'away', match.date)
        
        # Advanced form features
        home_form = self.get_advanced_form_features(match.home_team_id, match.date)
        away_form = self.get_advanced_form_features(match.away_team_id, match.date)
        
        # Momentum features
        home_momentum = self.get_momentum_features(match.home_team_id, match.date)
        away_momentum = self.get_momentum_features(match.away_team_id, match.date)
        
        # Head-to-head features
        h2h_features = self.get_h2h_advanced_features(
            match.home_team_id,
            match.away_team_id,
            match.date
        )
        
        # Time-based features
        time_features = self.get_time_features(match.date)
        
        # League position features
        home_position = self.get_league_position_features(
            match.home_team_id,
            match.league_id,
            match.date
        )
        away_position = self.get_league_position_features(
            match.away_team_id,
            match.league_id,
            match.date
        )
        
        # Combine all features
        all_features = np.concatenate([
            home_basic,
            away_basic,
            home_form,
            away_form,
            home_momentum,
            away_momentum,
            h2h_features,
            time_features,
            home_position,
            away_position
        ])
        
        return all_features
    
    def get_basic_features(self, team_id: int, venue: str, before_date: datetime) -> np.ndarray:
        """Get basic team features."""
        matches = self.session.query(Match).filter(
            Match.status == 'finished',
            Match.date < before_date
        )
        
        if venue == 'home':
            matches = matches.filter(Match.home_team_id == team_id)
        else:
            matches = matches.filter(Match.away_team_id == team_id)
        
        matches = matches.order_by(Match.date.desc()).limit(10).all()
        
        if not matches:
            return np.zeros(10)
        
        goals_scored = []
        goals_conceded = []
        points = []
        
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
        
        features = [
            np.mean(goals_scored),
            np.mean(goals_conceded),
            np.mean(points),
            sum(1 for p in points if p == 3) / len(points),
            sum(1 for p in points if p == 1) / len(points),
            sum(1 for g in goals_scored if g == 0) / len(goals_scored),
            sum(1 for g in goals_conceded if g == 0) / len(goals_conceded),
            np.std(goals_scored) if len(goals_scored) > 1 else 0,
            np.std(goals_conceded) if len(goals_conceded) > 1 else 0,
            len(matches) / 10
        ]
        
        return np.array(features)
    
    def get_advanced_form_features(self, team_id: int, before_date: datetime) -> np.ndarray:
        """
        Get advanced form features with weighted recent performance.
        
        Args:
            team_id: Team ID
            before_date: Date to consider matches before
            
        Returns:
            Advanced form features
        """
        matches = self.session.query(Match).filter(
            ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
            Match.status == 'finished',
            Match.date < before_date
        ).order_by(Match.date.desc()).limit(15).all()
        
        if not matches:
            return np.zeros(15)
        
        # Weighted form (recent matches weighted more)
        weights = np.exp(np.linspace(-1, 0, len(matches)))
        weights = weights / weights.sum()
        
        points = []
        goals_scored = []
        goals_conceded = []
        
        for match in matches:
            is_home = match.home_team_id == team_id
            
            if is_home:
                gs, gc = match.home_goals, match.away_goals
            else:
                gs, gc = match.away_goals, match.home_goals
            
            goals_scored.append(gs)
            goals_conceded.append(gc)
            
            if gs > gc:
                points.append(3)
            elif gs == gc:
                points.append(1)
            else:
                points.append(0)
        
        # Weighted averages
        weighted_points = np.average(points, weights=weights[:len(points)])
        weighted_gs = np.average(goals_scored, weights=weights[:len(goals_scored)])
        weighted_gc = np.average(goals_conceded, weights=weights[:len(goals_conceded)])
        
        # Last 3, 5, 10 matches performance
        last_3_points = np.mean(points[:3]) if len(points) >= 3 else 0
        last_5_points = np.mean(points[:5]) if len(points) >= 5 else 0
        last_10_points = np.mean(points[:10]) if len(points) >= 10 else 0
        
        # Scoring/conceding trends
        first_half_gs = np.mean(goals_scored[:len(goals_scored)//2]) if len(goals_scored) > 1 else 0
        second_half_gs = np.mean(goals_scored[len(goals_scored)//2:]) if len(goals_scored) > 1 else 0
        scoring_trend = second_half_gs - first_half_gs
        
        first_half_gc = np.mean(goals_conceded[:len(goals_conceded)//2]) if len(goals_conceded) > 1 else 0
        second_half_gc = np.mean(goals_conceded[len(goals_conceded)//2:]) if len(goals_conceded) > 1 else 0
        conceding_trend = second_half_gc - first_half_gc
        
        # Win/loss streaks
        current_streak = 0
        streak_type = 0  # 1 for win, -1 for loss, 0 for draw
        
        for p in points:
            if p == 3:
                if streak_type == 1:
                    current_streak += 1
                else:
                    current_streak = 1
                    streak_type = 1
            elif p == 0:
                if streak_type == -1:
                    current_streak += 1
                else:
                    current_streak = 1
                    streak_type = -1
            else:
                break
        
        features = [
            weighted_points,
            weighted_gs,
            weighted_gc,
            last_3_points,
            last_5_points,
            last_10_points,
            scoring_trend,
            conceding_trend,
            current_streak * streak_type,
            np.std(points) if len(points) > 1 else 0,
            np.std(goals_scored) if len(goals_scored) > 1 else 0,
            np.std(goals_conceded) if len(goals_conceded) > 1 else 0,
            sum(1 for gs, gc in zip(goals_scored, goals_conceded) if gs > 0 and gc > 0) / len(goals_scored),
            sum(1 for gs in goals_scored if gs >= 2) / len(goals_scored),
            sum(1 for gc in goals_conceded if gc >= 2) / len(goals_conceded)
        ]
        
        return np.array(features)
    
    def get_momentum_features(self, team_id: int, before_date: datetime) -> np.ndarray:
        """
        Calculate team momentum (improving/declining form).
        
        Args:
            team_id: Team ID
            before_date: Date to consider matches before
            
        Returns:
            Momentum features
        """
        matches = self.session.query(Match).filter(
            ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
            Match.status == 'finished',
            Match.date < before_date
        ).order_by(Match.date.desc()).limit(10).all()
        
        if len(matches) < 6:
            return np.zeros(5)
        
        points = []
        goals_diff = []
        
        for match in matches:
            is_home = match.home_team_id == team_id
            
            if is_home:
                gs, gc = match.home_goals, match.away_goals
            else:
                gs, gc = match.away_goals, match.home_goals
            
            goals_diff.append(gs - gc)
            
            if gs > gc:
                points.append(3)
            elif gs == gc:
                points.append(1)
            else:
                points.append(0)
        
        # Compare recent 3 vs previous 3
        recent_3_points = np.mean(points[:3])
        previous_3_points = np.mean(points[3:6])
        points_momentum = recent_3_points - previous_3_points
        
        # Goal difference momentum
        recent_3_gd = np.mean(goals_diff[:3])
        previous_3_gd = np.mean(goals_diff[3:6])
        gd_momentum = recent_3_gd - previous_3_gd
        
        # Linear trend in points
        x = np.arange(len(points))
        if len(points) > 1:
            points_trend = np.polyfit(x, points, 1)[0]
        else:
            points_trend = 0
        
        features = [
            points_momentum,
            gd_momentum,
            points_trend,
            recent_3_points,
            recent_3_gd
        ]
        
        return np.array(features)
    
    def get_h2h_advanced_features(
        self,
        home_team_id: int,
        away_team_id: int,
        before_date: datetime
    ) -> np.ndarray:
        """Get advanced head-to-head features."""
        h2h_matches = self.session.query(Match).filter(
            (
                (Match.home_team_id == home_team_id) & (Match.away_team_id == away_team_id)
            ) | (
                (Match.home_team_id == away_team_id) & (Match.away_team_id == home_team_id)
            ),
            Match.status == 'finished',
            Match.date < before_date
        ).order_by(Match.date.desc()).limit(10).all()
        
        if not h2h_matches:
            return np.zeros(8)
        
        home_wins = 0
        away_wins = 0
        draws = 0
        home_goals = 0
        away_goals = 0
        btts_count = 0
        over_25_count = 0
        
        for match in h2h_matches:
            if match.home_team_id == home_team_id:
                hg, ag = match.home_goals, match.away_goals
            else:
                hg, ag = match.away_goals, match.home_goals
            
            home_goals += hg
            away_goals += ag
            
            if hg > ag:
                home_wins += 1
            elif hg < ag:
                away_wins += 1
            else:
                draws += 1
            
            if hg > 0 and ag > 0:
                btts_count += 1
            
            if (hg + ag) > 2.5:
                over_25_count += 1
        
        n = len(h2h_matches)
        
        features = [
            home_wins / n,
            draws / n,
            away_wins / n,
            home_goals / n,
            away_goals / n,
            btts_count / n,
            over_25_count / n,
            n / 10  # Data availability
        ]
        
        return np.array(features)
    
    def get_time_features(self, match_date: datetime) -> np.ndarray:
        """Get time-based features."""
        # Day of week (weekend effect)
        day_of_week = match_date.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Month (season progression)
        month = match_date.month
        
        # Season stage (0-1, where 0 is start, 1 is end)
        # Assuming season runs Aug-May
        if month >= 8:
            season_progress = (month - 8) / 10
        else:
            season_progress = (month + 4) / 10
        
        features = [
            day_of_week / 6,
            is_weekend,
            month / 12,
            season_progress
        ]
        
        return np.array(features)
    
    def get_league_position_features(
        self,
        team_id: int,
        league_id: int,
        before_date: datetime
    ) -> np.ndarray:
        """Get league position and relative strength features."""
        # Get all teams in league
        teams = self.session.query(Team).filter_by(league_id=league_id).all()
        team_ids = [t.id for t in teams]
        
        # Calculate standings
        standings = {}
        
        for tid in team_ids:
            matches = self.session.query(Match).filter(
                ((Match.home_team_id == tid) | (Match.away_team_id == tid)),
                Match.status == 'finished',
                Match.league_id == league_id,
                Match.date < before_date
            ).all()
            
            points = 0
            for match in matches:
                is_home = match.home_team_id == tid
                
                if is_home:
                    if match.home_goals > match.away_goals:
                        points += 3
                    elif match.home_goals == match.away_goals:
                        points += 1
                else:
                    if match.away_goals > match.home_goals:
                        points += 3
                    elif match.away_goals == match.home_goals:
                        points += 1
            
            standings[tid] = points
        
        # Sort by points
        sorted_teams = sorted(standings.items(), key=lambda x: x[1], reverse=True)
        
        # Find position
        position = 1
        team_points = standings.get(team_id, 0)
        
        for i, (tid, pts) in enumerate(sorted_teams, 1):
            if tid == team_id:
                position = i
                break
        
        # Normalize position (0-1, where 0 is 1st place)
        num_teams = len(teams)
        normalized_position = (position - 1) / (num_teams - 1) if num_teams > 1 else 0
        
        # Points relative to leader
        leader_points = sorted_teams[0][1] if sorted_teams else 0
        points_from_leader = leader_points - team_points
        
        features = [
            normalized_position,
            team_points / (leader_points + 1),
            points_from_leader / (leader_points + 1)
        ]
        
        return np.array(features)
    
    def get_feature_names(self) -> List[str]:
        """Get all feature names."""
        basic_features = [
            'avg_goals_scored', 'avg_goals_conceded', 'avg_points',
            'win_rate', 'draw_rate', 'failed_to_score_rate',
            'clean_sheet_rate', 'goals_scored_std', 'goals_conceded_std',
            'data_completeness'
        ]
        
        form_features = [
            'weighted_points', 'weighted_goals_scored', 'weighted_goals_conceded',
            'last_3_points', 'last_5_points', 'last_10_points',
            'scoring_trend', 'conceding_trend', 'current_streak',
            'points_std', 'goals_scored_std', 'goals_conceded_std',
            'btts_rate', 'scored_2plus_rate', 'conceded_2plus_rate'
        ]
        
        momentum_features = [
            'points_momentum', 'gd_momentum', 'points_trend',
            'recent_3_points', 'recent_3_gd'
        ]
        
        h2h_features = [
            'h2h_home_win_rate', 'h2h_draw_rate', 'h2h_away_win_rate',
            'h2h_avg_home_goals', 'h2h_avg_away_goals',
            'h2h_btts_rate', 'h2h_over25_rate', 'h2h_data_availability'
        ]
        
        time_features = [
            'day_of_week_norm', 'is_weekend', 'month_norm', 'season_progress'
        ]
        
        position_features = [
            'league_position_norm', 'points_ratio_to_leader', 'points_gap_norm'
        ]
        
        all_features = []
        for prefix in ['home', 'away']:
            all_features.extend([f"{prefix}_{f}" for f in basic_features])
            all_features.extend([f"{prefix}_{f}" for f in form_features])
            all_features.extend([f"{prefix}_{f}" for f in momentum_features])
            all_features.extend([f"{prefix}_{f}" for f in position_features])
        
        all_features.extend(h2h_features)
        all_features.extend(time_features)
        
        return all_features


