"""Statistics calculation service."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.database import Match, Team, Prediction, UserBet, MatchStats
from database.connection import get_session


class StatsService:
    """Service for calculating statistics."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize stats service."""
        self.session = session or get_session()
    
    def get_overall_stats(self) -> Dict:
        """Get overall application statistics."""
        total_predictions = self.session.query(Prediction).count()
        total_bets = self.session.query(UserBet).count()
        
        # Calculate bet statistics
        won_bets = self.session.query(UserBet).filter_by(result='win').count()
        lost_bets = self.session.query(UserBet).filter_by(result='loss').count()
        
        win_rate = (won_bets / total_bets * 100) if total_bets > 0 else 0
        
        # Calculate ROI
        total_stake = self.session.query(func.sum(UserBet.stake)).filter(
            UserBet.result.in_(['win', 'loss'])
        ).scalar() or 0
        
        total_return = self.session.query(func.sum(UserBet.actual_return)).filter(
            UserBet.result == 'win'
        ).scalar() or 0
        
        roi = ((total_return - total_stake) / total_stake * 100) if total_stake > 0 else 0
        
        # Prediction accuracy (for finished matches)
        accurate_predictions = self._calculate_prediction_accuracy()
        
        return {
            'total_predictions': total_predictions,
            'total_bets': total_bets,
            'won_bets': won_bets,
            'lost_bets': lost_bets,
            'win_rate': round(win_rate, 1),
            'roi': round(roi, 1),
            'accuracy': round(accurate_predictions, 1),
            'total_stake': round(total_stake, 2),
            'total_return': round(total_return, 2),
            'profit': round(total_return - total_stake, 2)
        }
    
    def _calculate_prediction_accuracy(self) -> float:
        """Calculate prediction accuracy for finished matches."""
        predictions = self.session.query(Prediction).all()
        
        if not predictions:
            return 0.0
        
        correct = 0
        total = 0
        
        for pred in predictions:
            match = self.session.query(Match).filter_by(id=pred.match_id).first()
            
            if not match or match.status != 'finished':
                continue
            
            total += 1
            
            # Determine predicted outcome
            probs = {
                'home': pred.home_win_prob,
                'draw': pred.draw_prob,
                'away': pred.away_win_prob
            }
            predicted_outcome = max(probs, key=probs.get)
            
            # Determine actual outcome
            if match.home_goals > match.away_goals:
                actual_outcome = 'home'
            elif match.home_goals < match.away_goals:
                actual_outcome = 'away'
            else:
                actual_outcome = 'draw'
            
            if predicted_outcome == actual_outcome:
                correct += 1
        
        return (correct / total * 100) if total > 0 else 0.0
    
    def get_team_stats(self, team_id: int, last_n: int = 10) -> Dict:
        """
        Get statistics for a specific team.
        
        Args:
            team_id: Team ID
            last_n: Number of recent matches to analyze
            
        Returns:
            Dictionary with team statistics
        """
        team = self.session.query(Team).filter_by(id=team_id).first()
        
        if not team:
            return {}
        
        # Get recent matches
        matches = self.session.query(Match).filter(
            ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
            Match.status == 'finished'
        ).order_by(Match.date.desc()).limit(last_n).all()
        
        if not matches:
            return {'team_name': team.name, 'matches_played': 0}
        
        # Calculate statistics
        wins = 0
        draws = 0
        losses = 0
        goals_scored = 0
        goals_conceded = 0
        clean_sheets = 0
        failed_to_score = 0
        
        for match in matches:
            is_home = match.home_team_id == team_id
            
            if is_home:
                team_goals = match.home_goals
                opp_goals = match.away_goals
            else:
                team_goals = match.away_goals
                opp_goals = match.home_goals
            
            goals_scored += team_goals
            goals_conceded += opp_goals
            
            if opp_goals == 0:
                clean_sheets += 1
            
            if team_goals == 0:
                failed_to_score += 1
            
            if team_goals > opp_goals:
                wins += 1
            elif team_goals == opp_goals:
                draws += 1
            else:
                losses += 1
        
        matches_played = len(matches)
        points = wins * 3 + draws
        
        return {
            'team_name': team.name,
            'matches_played': matches_played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_scored': goals_scored,
            'goals_conceded': goals_conceded,
            'goal_difference': goals_scored - goals_conceded,
            'points': points,
            'ppg': round(points / matches_played, 2) if matches_played > 0 else 0,
            'win_rate': round(wins / matches_played * 100, 1) if matches_played > 0 else 0,
            'clean_sheets': clean_sheets,
            'failed_to_score': failed_to_score,
            'avg_goals_scored': round(goals_scored / matches_played, 2) if matches_played > 0 else 0,
            'avg_goals_conceded': round(goals_conceded / matches_played, 2) if matches_played > 0 else 0
        }
    
    def get_league_table(self, league_id: int) -> List[Dict]:
        """
        Get league table standings.
        
        Args:
            league_id: League ID
            
        Returns:
            List of team standings
        """
        teams = self.session.query(Team).filter_by(league_id=league_id).all()
        
        standings = []
        
        for team in teams:
            # Get all finished matches for this team
            matches = self.session.query(Match).filter(
                ((Match.home_team_id == team.id) | (Match.away_team_id == team.id)),
                Match.status == 'finished',
                Match.league_id == league_id
            ).all()
            
            wins = 0
            draws = 0
            losses = 0
            goals_for = 0
            goals_against = 0
            
            for match in matches:
                is_home = match.home_team_id == team.id
                
                if is_home:
                    team_goals = match.home_goals
                    opp_goals = match.away_goals
                else:
                    team_goals = match.away_goals
                    opp_goals = match.home_goals
                
                goals_for += team_goals
                goals_against += opp_goals
                
                if team_goals > opp_goals:
                    wins += 1
                elif team_goals == opp_goals:
                    draws += 1
                else:
                    losses += 1
            
            points = wins * 3 + draws
            played = wins + draws + losses
            
            standings.append({
                'team_id': team.id,
                'team_name': team.name,
                'played': played,
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'goal_difference': goals_for - goals_against,
                'points': points
            })
        
        # Sort by points, then goal difference, then goals for
        standings.sort(key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)
        
        # Add position
        for i, standing in enumerate(standings, 1):
            standing['position'] = i
        
        return standings
    
    def get_betting_stats(self, days: int = 30) -> Dict:
        """
        Get betting statistics for a time period.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with betting statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        bets = self.session.query(UserBet).filter(
            UserBet.created_at >= cutoff_date
        ).all()
        
        if not bets:
            return {
                'total_bets': 0,
                'won': 0,
                'lost': 0,
                'pending': 0,
                'win_rate': 0,
                'roi': 0,
                'profit': 0
            }
        
        total = len(bets)
        won = sum(1 for b in bets if b.result == 'win')
        lost = sum(1 for b in bets if b.result == 'loss')
        pending = sum(1 for b in bets if b.result == 'pending')
        
        total_stake = sum(b.stake for b in bets if b.result in ['win', 'loss'])
        total_return = sum(b.actual_return or 0 for b in bets if b.result == 'win')
        
        win_rate = (won / (won + lost) * 100) if (won + lost) > 0 else 0
        roi = ((total_return - total_stake) / total_stake * 100) if total_stake > 0 else 0
        profit = total_return - total_stake
        
        return {
            'total_bets': total,
            'won': won,
            'lost': lost,
            'pending': pending,
            'win_rate': round(win_rate, 1),
            'roi': round(roi, 1),
            'profit': round(profit, 2),
            'total_stake': round(total_stake, 2),
            'total_return': round(total_return, 2)
        }
    
    def get_form_guide(self, team_id: int, last_n: int = 5) -> List[str]:
        """
        Get team form guide (W/D/L).
        
        Args:
            team_id: Team ID
            last_n: Number of recent matches
            
        Returns:
            List of results ['W', 'D', 'L']
        """
        matches = self.session.query(Match).filter(
            ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
            Match.status == 'finished'
        ).order_by(Match.date.desc()).limit(last_n).all()
        
        form = []
        
        for match in matches:
            is_home = match.home_team_id == team_id
            
            if is_home:
                if match.home_goals > match.away_goals:
                    form.append('W')
                elif match.home_goals == match.away_goals:
                    form.append('D')
                else:
                    form.append('L')
            else:
                if match.away_goals > match.home_goals:
                    form.append('W')
                elif match.away_goals == match.home_goals:
                    form.append('D')
                else:
                    form.append('L')
        
        return form



