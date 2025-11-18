"""Data access service."""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session
from models.database import Match, Team, League, Prediction, UserBet, MatchStats
from database.connection import get_session


class DataService:
    """Service for data access operations."""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize data service."""
        self.session = session or get_session()
    
    def get_upcoming_matches(self, limit: int = 10, league_id: Optional[int] = None) -> List[Match]:
        """
        Get upcoming scheduled matches.
        
        Args:
            limit: Maximum number of matches to return
            league_id: Filter by league ID (optional)
            
        Returns:
            List of upcoming matches
        """
        query = self.session.query(Match).filter(
            Match.status == 'scheduled',
            Match.date >= datetime.now()
        )
        
        if league_id:
            query = query.filter(Match.league_id == league_id)
        
        return query.order_by(Match.date).limit(limit).all()
    
    def get_recent_matches(self, limit: int = 10, league_id: Optional[int] = None) -> List[Match]:
        """
        Get recent finished matches.
        
        Args:
            limit: Maximum number of matches to return
            league_id: Filter by league ID (optional)
            
        Returns:
            List of recent matches
        """
        query = self.session.query(Match).filter(
            Match.status == 'finished'
        )
        
        if league_id:
            query = query.filter(Match.league_id == league_id)
        
        return query.order_by(Match.date.desc()).limit(limit).all()
    
    def get_match_by_id(self, match_id: int) -> Optional[Match]:
        """Get match by ID."""
        return self.session.query(Match).filter_by(id=match_id).first()
    
    def get_team_by_id(self, team_id: int) -> Optional[Team]:
        """Get team by ID."""
        return self.session.query(Team).filter_by(id=team_id).first()
    
    def get_league_by_id(self, league_id: int) -> Optional[League]:
        """Get league by ID."""
        return self.session.query(League).filter_by(id=league_id).first()
    
    def get_all_leagues(self) -> List[League]:
        """Get all leagues."""
        return self.session.query(League).all()
    
    def get_teams_by_league(self, league_id: int) -> List[Team]:
        """Get all teams in a league."""
        return self.session.query(Team).filter_by(league_id=league_id).all()
    
    def get_team_matches(
        self,
        team_id: int,
        limit: int = 10,
        status: str = 'finished'
    ) -> List[Match]:
        """
        Get matches for a specific team.
        
        Args:
            team_id: Team ID
            limit: Maximum number of matches
            status: Match status filter
            
        Returns:
            List of matches
        """
        return self.session.query(Match).filter(
            or_(
                Match.home_team_id == team_id,
                Match.away_team_id == team_id
            ),
            Match.status == status
        ).order_by(Match.date.desc()).limit(limit).all()
    
    def search_matches(
        self,
        team_name: Optional[str] = None,
        league_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        status: Optional[str] = None
    ) -> List[Match]:
        """
        Search matches with filters.
        
        Args:
            team_name: Team name to search for
            league_id: League ID filter
            date_from: Start date filter
            date_to: End date filter
            status: Match status filter
            
        Returns:
            List of matching matches
        """
        query = self.session.query(Match)
        
        if team_name:
            teams = self.session.query(Team).filter(
                Team.name.ilike(f'%{team_name}%')
            ).all()
            team_ids = [t.id for t in teams]
            
            query = query.filter(
                or_(
                    Match.home_team_id.in_(team_ids),
                    Match.away_team_id.in_(team_ids)
                )
            )
        
        if league_id:
            query = query.filter(Match.league_id == league_id)
        
        if date_from:
            query = query.filter(Match.date >= date_from)
        
        if date_to:
            query = query.filter(Match.date <= date_to)
        
        if status:
            query = query.filter(Match.status == status)
        
        return query.order_by(Match.date.desc()).all()
    
    def get_prediction_for_match(self, match_id: int) -> Optional[Prediction]:
        """Get prediction for a match."""
        return self.session.query(Prediction).filter_by(match_id=match_id).first()
    
    def get_all_predictions(self, limit: int = 100) -> List[Prediction]:
        """Get all predictions."""
        return self.session.query(Prediction).order_by(
            Prediction.prediction_date.desc()
        ).limit(limit).all()
    
    def save_prediction(self, prediction: Prediction) -> Prediction:
        """Save or update prediction."""
        self.session.add(prediction)
        self.session.commit()
        return prediction
    
    def get_user_bets(
        self,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[UserBet]:
        """
        Get user bets.
        
        Args:
            status: Filter by bet status ('pending', 'win', 'loss')
            limit: Maximum number of bets
            
        Returns:
            List of user bets
        """
        query = self.session.query(UserBet)
        
        if status:
            query = query.filter(UserBet.result == status)
        
        return query.order_by(UserBet.created_at.desc()).limit(limit).all()
    
    def save_user_bet(self, bet: UserBet) -> UserBet:
        """Save user bet."""
        self.session.add(bet)
        self.session.commit()
        return bet
    
    def update_bet_result(self, bet_id: int, result: str, actual_return: float):
        """Update bet result."""
        bet = self.session.query(UserBet).filter_by(id=bet_id).first()
        if bet:
            bet.result = result
            bet.actual_return = actual_return
            bet.settled_at = datetime.now()
            self.session.commit()
    
    def get_match_stats(self, match_id: int) -> List[MatchStats]:
        """Get statistics for a match."""
        return self.session.query(MatchStats).filter_by(match_id=match_id).all()
    
    def get_matches_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Match]:
        """Get matches within date range."""
        return self.session.query(Match).filter(
            and_(
                Match.date >= start_date,
                Match.date <= end_date
            )
        ).order_by(Match.date).all()
    
    def get_all_matches(self, limit: int = 100) -> List[Match]:
        """
        Get all matches.
        
        Args:
            limit: Maximum number of matches to return
            
        Returns:
            List of matches
        """
        return self.session.query(Match).order_by(Match.date.desc()).limit(limit).all()
    
    def get_matches_by_status(self, status: str, limit: int = 100) -> List[Match]:
        """
        Get matches by status.
        
        Args:
            status: Match status ('scheduled', 'finished', 'in_play')
            limit: Maximum number of matches to return
            
        Returns:
            List of matches with given status
        """
        return self.session.query(Match).filter(
            Match.status == status
        ).order_by(Match.date.desc()).limit(limit).all()


