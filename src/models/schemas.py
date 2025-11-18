"""Pydantic schemas for data validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TeamSchema(BaseModel):
    """Team schema."""
    id: int
    name: str
    league_id: Optional[int] = None
    logo_path: Optional[str] = None
    founded: Optional[int] = None
    stadium: Optional[str] = None
    
    class Config:
        from_attributes = True


class MatchSchema(BaseModel):
    """Match schema."""
    id: int
    date: datetime
    home_team_id: int
    away_team_id: int
    league_id: int
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    status: str = 'scheduled'
    
    class Config:
        from_attributes = True


class PredictionSchema(BaseModel):
    """Prediction schema."""
    id: Optional[int] = None
    match_id: int
    home_win_prob: float = Field(ge=0, le=1)
    draw_prob: float = Field(ge=0, le=1)
    away_win_prob: float = Field(ge=0, le=1)
    btts_prob: Optional[float] = Field(None, ge=0, le=1)
    over_2_5_prob: Optional[float] = Field(None, ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    
    class Config:
        from_attributes = True


class UserBetSchema(BaseModel):
    """User bet schema."""
    id: Optional[int] = None
    match_id: int
    bet_type: str
    prediction: str
    stake: float = Field(gt=0)
    odds: float = Field(gt=1.0)
    result: str = 'pending'
    
    class Config:
        from_attributes = True



