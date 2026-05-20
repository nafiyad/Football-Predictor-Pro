"""Live data ingestion from Football-Data.org."""
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from models.database import Match, Team, League
from database.connection import get_session
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LiveDataIngestor:
    """Ingest live football data from Football-Data.org API."""
    
    LEAGUE_CODES = {
        'Premier League': 'PL',
        'La Liga': 'PD', 
        'Bundesliga': 'BL1',
        'Serie A': 'SA',
        'Ligue 1': 'FL1'
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('FOOTBALL_DATA_API_KEY', '')
        self.base_url = "https://api.football-data.org/v4"
        self.session = get_session()
    
    def fetch_competition_matches(self, competition_code: str, days_before: int = 7, days_after: int = 14) -> List[Dict]:
        """Fetch matches for a competition."""
        if not self.api_key:
            logger.error("API key required for live data")
            return []
        
        date_from = (datetime.now() - timedelta(days=days_before)).strftime('%Y-%m-%d')
        date_to = (datetime.now() + timedelta(days=days_after)).strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/competitions/{competition_code}/matches"
        headers = {"X-Auth-Token": self.api_key}
        params = {"dateFrom": date_from, "dateTo": date_to, "status": "SCHEDULED_IN_PLAY_FINISHED"}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            matches = data.get('matches', [])
            logger.info(f"Fetched {len(matches)} matches for {competition_code}")
            return matches
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching matches: {e}")
            return []
    
    def import_all_leagues(self, force_update: bool = False) -> Dict[str, int]:
        """Import all supported leagues."""
        results = {}
        for comp_name, code in self.LEAGUE_CODES.items():
            league = self.session.query(League).filter_by(name=comp_name).first()
            if not league:
                league = League(name=comp_name, country=comp_name.split()[-1] if ' ' in comp_name else 'Unknown')
                self.session.add(league)
                self.session.commit()
            
            matches_data = self.fetch_competition_matches(code)
            imported = 0
            for match_dict in matches_data:
                utc_date = match_dict.get('utcDate')
                if not utc_date:
                    continue
                
                if not force_update:
                    existing = self.session.query(Match).filter(
                        Match.date == datetime.fromisoformat(utc_date.replace('Z', '+00:00'))
                    ).first()
                    if existing:
                        continue
                
                home_name = match_dict.get('homeTeam', {}).get('name')
                away_name = match_dict.get('awayTeam', {}).get('name')
                if not home_name or not away_name:
                    continue
                
                home_team = self.session.query(Team).filter_by(name=home_name, league_id=league.id).first()
                if not home_team:
                    home_team = Team(name=home_name, league_id=league.id)
                    self.session.add(home_team)
                
                away_team = self.session.query(Team).filter_by(name=away_name, league_id=league.id).first()
                if not away_team:
                    away_team = Team(name=away_name, league_id=league.id)
                    self.session.add(away_team)
                
                self.session.commit()
                
                score = match_dict.get('score', {}).get('fullTime', {})
                match = Match(
                    date=datetime.fromisoformat(utc_date.replace('Z', '+00:00')),
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    league_id=league.id,
                    home_goals=score.get('home'),
                    away_goals=score.get('away'),
                    status='finished' if score.get('home') is not None else 'scheduled'
                )
                self.session.add(match)
                imported += 1
            
            self.session.commit()
            results[comp_name] = imported
        
        return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Import live football data')
    parser.add_argument('--api-key', help='Football-Data.org API key')
    parser.add_argument('--force', action='store_true', help='Force update existing')
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get('FOOTBALL_DATA_API_KEY')
    if not api_key:
        print("Error: API key required. Set FOOTBALL_DATA_API_KEY or use --api-key")
        exit(1)
    
    ingestor = LiveDataIngestor(api_key=api_key)
    results = ingestor.import_all_leagues(args.force)
    for comp, count in results.items():
        print(f"{comp}: {count} matches")