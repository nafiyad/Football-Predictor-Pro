"""Simple script to import real football data with your API key."""
import sys
import os
from datetime import datetime, timedelta
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from database.connection import get_session, init_db
from models.database import League, Team, Match

# Your API key
API_KEY = "1d29a1036d08434caae76606c972eedd"

def fetch_matches(competition_code, date_from, date_to):
    """Fetch matches from Football-Data.org."""
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/matches"
    
    headers = {
        "X-Auth-Token": API_KEY
    }
    
    params = {
        "dateFrom": date_from,
        "dateTo": date_to
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("matches", [])
    except Exception as e:
        print(f"  Error: {e}")
        return []


def import_data():
    """Import real football data."""
    print("\n" + "="*70)
    print("IMPORTING REAL FOOTBALL DATA")
    print("="*70 + "\n")
    
    # Initialize
    init_db()
    session = get_session()
    
    # Date range
    date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    date_to = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    print(f"Fetching matches from {date_from} to {date_to}\n")
    
    leagues = {
        "Premier League": ("PL", "England"),
        "La Liga": ("PD", "Spain"),
        "Bundesliga": ("BL1", "Germany"),
        "Serie A": ("SA", "Italy"),
        "Ligue 1": ("FL1", "France")
    }
    
    total_matches = 0
    total_teams = 0
    
    for league_name, (code, country) in leagues.items():
        print(f"\nFetching {league_name}...")
        
        matches_data = fetch_matches(code, date_from, date_to)
        
        if not matches_data:
            print(f"  ⚠ No data fetched")
            continue
        
        # Get or create league
        league = session.query(League).filter_by(name=league_name).first()
        if not league:
            league = League(name=league_name, country=country, season="2024/2025")
            session.add(league)
            session.flush()
        
        matches_imported = 0
        teams_created = 0
        
        for match_data in matches_data:
            try:
                # Parse match data
                home_team_name = match_data.get("homeTeam", {}).get("name")
                away_team_name = match_data.get("awayTeam", {}).get("name")
                
                if not home_team_name or not away_team_name:
                    continue
                
                # Get or create home team
                home_team = session.query(Team).filter_by(
                    name=home_team_name,
                    league_id=league.id
                ).first()
                
                if not home_team:
                    home_team = Team(name=home_team_name, league_id=league.id)
                    session.add(home_team)
                    session.flush()
                    teams_created += 1
                
                # Get or create away team
                away_team = session.query(Team).filter_by(
                    name=away_team_name,
                    league_id=league.id
                ).first()
                
                if not away_team:
                    away_team = Team(name=away_team_name, league_id=league.id)
                    session.add(away_team)
                    session.flush()
                    teams_created += 1
                
                # Parse date
                utc_date = match_data.get("utcDate")
                if utc_date:
                    match_date = datetime.fromisoformat(utc_date.replace('Z', '+00:00'))
                else:
                    continue
                
                # Get score
                score = match_data.get("score", {}).get("fullTime", {})
                home_goals = score.get("home")
                away_goals = score.get("away")
                
                # Determine status
                status_map = {
                    "FINISHED": "finished",
                    "SCHEDULED": "scheduled",
                    "TIMED": "scheduled",
                    "IN_PLAY": "live",
                    "PAUSED": "live"
                }
                status = status_map.get(match_data.get("status"), "scheduled")
                
                # Check if match exists
                existing = session.query(Match).filter_by(
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    date=match_date
                ).first()
                
                if existing:
                    # Update
                    existing.home_goals = home_goals
                    existing.away_goals = away_goals
                    existing.status = status
                else:
                    # Create new
                    match = Match(
                        date=match_date,
                        home_team_id=home_team.id,
                        away_team_id=away_team.id,
                        league_id=league.id,
                        home_goals=home_goals,
                        away_goals=away_goals,
                        status=status
                    )
                    session.add(match)
                    matches_imported += 1
            
            except Exception as e:
                print(f"  Error processing match: {e}")
                continue
        
        session.commit()
        print(f"  ✓ Imported {matches_imported} matches")
        print(f"  ✓ Created {teams_created} teams")
        
        total_matches += matches_imported
        total_teams += teams_created
    
    session.close()
    
    print("\n" + "="*70)
    print(f"✓ IMPORT COMPLETED!")
    print(f"  Total matches imported: {total_matches}")
    print(f"  Total teams created: {total_teams}")
    print("="*70 + "\n")


if __name__ == '__main__':
    import_data()


