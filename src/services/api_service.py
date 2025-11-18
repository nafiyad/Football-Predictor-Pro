"""API service for fetching real football data."""
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FootballAPIService:
    """Service for fetching real football data from APIs."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize API service.
        
        Args:
            api_key: API key for the football data service
        """
        self.api_key = api_key
        
        # API-Football (RapidAPI) - Most comprehensive
        self.api_football_base = "https://v3.football.api-sports.io"
        
        # Football-Data.org - Free tier available
        self.football_data_base = "https://api.football-data.org/v4"
        
        # Free alternative: API-FOOTBALL (limited)
        self.free_api_base = "https://api-football-v1.p.rapidapi.com/v3"
    
    def fetch_matches_api_football(
        self,
        league_id: int,
        season: int = 2024,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch matches from API-Football (RapidAPI).
        
        Requires API key from: https://rapidapi.com/api-sports/api/api-football
        
        Args:
            league_id: League ID (e.g., 39 for Premier League)
            season: Season year
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            
        Returns:
            List of match dictionaries
        """
        if not self.api_key:
            logger.error("API key required for API-Football")
            return []
        
        url = f"{self.api_football_base}/fixtures"
        
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        
        params = {
            "league": league_id,
            "season": season
        }
        
        if date_from:
            params["from"] = date_from
        if date_to:
            params["to"] = date_to
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("response"):
                logger.info(f"Fetched {len(data['response'])} matches from API-Football")
                return data["response"]
            
            return []
        
        except Exception as e:
            logger.error(f"Error fetching from API-Football: {e}")
            return []
    
    def fetch_matches_football_data_org(
        self,
        competition_code: str = "PL",
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch matches from Football-Data.org (Free tier available).
        
        Get free API key from: https://www.football-data.org/client/register
        
        Args:
            competition_code: Competition code (PL, PD, BL1, SA, FL1)
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            
        Returns:
            List of match dictionaries
        """
        url = f"{self.football_data_base}/competitions/{competition_code}/matches"
        
        headers = {}
        if self.api_key:
            headers["X-Auth-Token"] = self.api_key
        
        params = {}
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("matches"):
                logger.info(f"Fetched {len(data['matches'])} matches from Football-Data.org")
                return data["matches"]
            
            return []
        
        except Exception as e:
            logger.error(f"Error fetching from Football-Data.org: {e}")
            return []
    
    def parse_api_football_match(self, match_data: Dict) -> Dict:
        """
        Parse API-Football match data to our format.
        
        Args:
            match_data: Raw match data from API
            
        Returns:
            Parsed match dictionary
        """
        fixture = match_data.get("fixture", {})
        teams = match_data.get("teams", {})
        goals = match_data.get("goals", {})
        
        return {
            "date": fixture.get("date"),
            "home_team": teams.get("home", {}).get("name"),
            "away_team": teams.get("away", {}).get("name"),
            "home_goals": goals.get("home"),
            "away_goals": goals.get("away"),
            "status": fixture.get("status", {}).get("short"),
            "league": match_data.get("league", {}).get("name"),
            "venue": fixture.get("venue", {}).get("name"),
            "referee": fixture.get("referee")
        }
    
    def parse_football_data_org_match(self, match_data: Dict) -> Dict:
        """
        Parse Football-Data.org match data to our format.
        
        Args:
            match_data: Raw match data from API
            
        Returns:
            Parsed match dictionary
        """
        score = match_data.get("score", {}).get("fullTime", {})
        
        return {
            "date": match_data.get("utcDate"),
            "home_team": match_data.get("homeTeam", {}).get("name"),
            "away_team": match_data.get("awayTeam", {}).get("name"),
            "home_goals": score.get("home"),
            "away_goals": score.get("away"),
            "status": match_data.get("status"),
            "league": match_data.get("competition", {}).get("name"),
            "venue": match_data.get("venue")
        }


# League ID mappings for different APIs
API_FOOTBALL_LEAGUES = {
    "Premier League": 39,
    "La Liga": 140,
    "Bundesliga": 78,
    "Serie A": 135,
    "Ligue 1": 61
}

FOOTBALL_DATA_ORG_CODES = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1"
}



