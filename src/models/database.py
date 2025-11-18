"""Database models using SQLAlchemy."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class League(Base):
    """League model."""
    __tablename__ = 'leagues'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100))
    season = Column(String(20))
    logo_path = Column(String(255))
    
    teams = relationship("Team", back_populates="league")
    matches = relationship("Match", back_populates="league")
    
    def __repr__(self):
        return f"<League(id={self.id}, name='{self.name}', country='{self.country}')>"


class Team(Base):
    """Team model."""
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.id'))
    logo_path = Column(String(255))
    founded = Column(Integer)
    stadium = Column(String(100))
    
    league = relationship("League", back_populates="teams")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    
    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"


class Match(Base):
    """Match model."""
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    home_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False)
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    status = Column(String(20), default='scheduled')  # 'scheduled', 'live', 'finished'
    round = Column(String(50))
    referee = Column(String(100))
    stadium = Column(String(100))
    
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    league = relationship("League", back_populates="matches")
    stats = relationship("MatchStats", back_populates="match", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="match", cascade="all, delete-orphan")
    user_bets = relationship("UserBet", back_populates="match", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Match(id={self.id}, {self.home_team.name if self.home_team else 'Home'} vs {self.away_team.name if self.away_team else 'Away'})>"


class MatchStats(Base):
    """Match statistics model."""
    __tablename__ = 'match_stats'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    possession = Column(Float)
    shots = Column(Integer)
    shots_on_target = Column(Integer)
    corners = Column(Integer)
    fouls = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    offsides = Column(Integer)
    xg = Column(Float)  # Expected Goals
    
    match = relationship("Match", back_populates="stats")
    team = relationship("Team")
    
    def __repr__(self):
        return f"<MatchStats(id={self.id}, match_id={self.match_id}, team_id={self.team_id})>"


class Prediction(Base):
    """Prediction model."""
    __tablename__ = 'predictions'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    home_win_prob = Column(Float)
    draw_prob = Column(Float)
    away_win_prob = Column(Float)
    btts_prob = Column(Float)  # Both Teams To Score
    over_2_5_prob = Column(Float)
    under_2_5_prob = Column(Float)
    predicted_home_goals = Column(Float)
    predicted_away_goals = Column(Float)
    confidence = Column(Float)
    model_version = Column(String(50))
    
    match = relationship("Match", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, match_id={self.match_id}, confidence={self.confidence})>"


class UserBet(Base):
    """User bet tracking model."""
    __tablename__ = 'user_bets'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    bet_type = Column(String(50))  # '1X2', 'BTTS', 'O/U 2.5', etc.
    prediction = Column(String(50))  # 'Home', 'Draw', 'Away', 'Yes', 'No', 'Over', 'Under'
    stake = Column(Float)
    odds = Column(Float)
    potential_return = Column(Float)
    result = Column(String(20))  # 'win', 'loss', 'pending', 'void'
    actual_return = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    settled_at = Column(DateTime)
    
    match = relationship("Match", back_populates="user_bets")
    
    def __repr__(self):
        return f"<UserBet(id={self.id}, match_id={self.match_id}, bet_type='{self.bet_type}', result='{self.result}')>"



