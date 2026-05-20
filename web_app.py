"""FastAPI web application for Football Predictor Pro."""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.data_service import DataService
from services.prediction_service import PredictionService
from services.bet_calculator import BetValueCalculator
from database.connection import init_db

app = FastAPI(title="Football Predictor Pro API", version="2.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

data_service = DataService()
prediction_service = PredictionService()
bet_calculator = BetValueCalculator()


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/")
async def root():
    return {"name": "Football Predictor Pro API", "version": "2.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/leagues")
async def get_leagues():
    leagues = data_service.get_leagues()
    return [{"id": l.id, "name": l.name, "country": l.country} for l in leagues]


@app.get("/matches/upcoming")
async def get_upcoming_matches(league_id: Optional[int] = None, limit: int = 10):
    matches = data_service.get_upcoming_matches(limit=limit, league_id=league_id)
    return [{
        "id": m.id,
        "home_team": m.home_team.name if m.home_team else "Unknown",
        "away_team": m.away_team.name if m.away_team else "Unknown",
        "league": m.league.name if m.league else "Unknown",
        "date": m.date.isoformat() if m.date else "",
        "status": m.status
    } for m in matches]


@app.get("/matches/recent")
async def get_recent_matches(league_id: Optional[int] = None, limit: int = 10):
    matches = data_service.get_recent_matches(limit=limit, league_id=league_id)
    return [{
        "id": m.id,
        "home_team": m.home_team.name if m.home_team else "Unknown",
        "away_team": m.away_team.name if m.away_team else "Unknown",
        "date": m.date.isoformat() if m.date else "",
        "home_goals": m.home_goals,
        "away_goals": m.away_goals,
        "status": m.status
    } for m in matches]


@app.get("/predictions/{match_id}")
async def get_prediction(match_id: int):
    prediction = prediction_service.get_match_prediction(match_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    match = data_service.get_match_by_id(match_id)
    return {
        "match_id": match_id,
        "home_team": match.home_team.name if match and match.home_team else "Unknown",
        "away_team": match.away_team.name if match and match.away_team else "Unknown",
        "home_win_prob": prediction.home_win_prob,
        "draw_prob": prediction.draw_prob,
        "away_win_prob": prediction.away_win_prob,
        "btts_prob": prediction.btts_prob,
        "over_2_5_prob": prediction.over_2_5_prob,
        "confidence": prediction.confidence
    }


@app.post("/predictions/bet-analysis")
async def analyze_bet(match_id: int, odds_home: float, odds_draw: float, odds_away: float, bankroll: float = 1000.0):
    prediction = prediction_service.get_match_prediction(match_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    recommendations = bet_calculator.analyze_prediction(prediction, odds_home, odds_draw, odds_away, bankroll)
    return {"match_id": match_id, "bets": [{
        "selection": r.selection,
        "probability": r.probability,
        "odds": r.bookmaker_odds,
        "ev": r.expected_value,
        "confidence": r.confidence
    } for r in recommendations]}


@app.get("/teams/{team_id}/stats")
async def get_team_stats(team_id: int):
    team = data_service.get_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    recent = data_service.get_team_matches(team_id, limit=5, status='finished')
    if not recent:
        return {"team": team.name, "form": "", "avg_goals": 0, "win_rate": 0}
    
    goals = []
    results = []
    for m in recent:
        is_home = m.home_team_id == team_id
        gs = m.home_goals if is_home else m.away_goals
        gc = m.away_goals if is_home else m.home_goals
        goals.append((gs or 0, gc or 0))
        if gs > gc:
            results.append('W')
        elif gs == gc:
            results.append('D')
        else:
            results.append('L')
    
    wins = results.count('W')
    return {
        "team": team.name,
        "form": "".join(reversed(results)),
        "avg_goals_scored": sum(g[0] for g in goals) / len(goals) if goals else 0,
        "avg_goals_conceded": sum(g[1] for g in goals) / len(goals) if goals else 0,
        "win_rate": wins / len(results) if results else 0
    }


@app.get("/teams/{team_id}/timeline")
async def get_team_timeline(team_id: int, limit: int = 10):
    team = data_service.get_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    matches = data_service.get_team_matches(team_id, limit=limit, status='finished')
    timeline = []
    for m in reversed(matches):
        is_home = m.home_team_id == team_id
        opp = m.away_team.name if is_home else m.home_team.name
        our = m.home_goals if is_home else m.away_goals
        their = m.away_goals if is_home else m.home_goals
        
        if our > their:
            result = 'W'
        elif our == their:
            result = 'D'
        else:
            result = 'L'
        
        pred = data_service.get_prediction_for_match(m.id)
        win_prob = pred.home_win_prob if is_home else pred.away_win_prob if pred else 0.5
        
        timeline.append({
            "date": m.date.isoformat(),
            "opponent": opp,
            "result": result,
            "win_probability": win_prob
        })
    
    return timeline


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)