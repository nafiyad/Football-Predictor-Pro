"""Clean database and reimport with correct data only."""
import sys
import os
from datetime import datetime, timedelta
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from database.connection import get_session, init_db
from models.database import League, Team, Match, MatchStats, Prediction, UserBet

# Your API key
API_KEY = "1d29a1036d08434caae76606c972eedd"


def clear_all_data():
    """Clear all data from database."""
    print("\n" + "="*70)
    print("CLEARING ALL DATA")
    print("="*70 + "\n")
    
    init_db()
    session = get_session()
    
    try:
        # Delete in correct order (respect foreign keys)
        print("Deleting predictions...")
        session.query(Prediction).delete()
        
        print("Deleting user bets...")
        session.query(UserBet).delete()
        
        print("Deleting match stats...")
        session.query(MatchStats).delete()
        
        print("Deleting matches...")
        session.query(Match).delete()
        
        print("Deleting teams...")
        session.query(Team).delete()
        
        print("Deleting leagues...")
        session.query(League).delete()
        
        session.commit()
        print("✓ All data cleared\n")
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def fetch_league_standings(competition_code):
    """Fetch current league standings to get correct teams."""
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/standings"
    
    headers = {
        "X-Auth-Token": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Get teams from standings
        standings = data.get("standings", [])
        if standings:
            table = standings[0].get("table", [])
            return [team_data.get("team", {}).get("name") for team_data in table]
        
        return []
    except Exception as e:
        print(f"  Error fetching standings: {e}")
        return []


def fetch_matches(competition_code, season="2024"):
    """Fetch matches for a specific season."""
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/matches"
    
    headers = {
        "X-Auth-Token": API_KEY
    }
    
    params = {
        "season": season
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("matches", [])
    except Exception as e:
        print(f"  Error: {e}")
        return []


def import_correct_data():
    """Import only correct data with proper validation."""
    print("\n" + "="*70)
    print("IMPORTING CORRECT FOOTBALL DATA")
    print("="*70 + "\n")
    
    init_db()
    session = get_session()
    
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
        print(f"\n{'='*70}")
        print(f"Processing {league_name}")
        print('='*70)
        
        # Get current season teams from standings
        print(f"  Fetching current teams from standings...")
        valid_teams = fetch_league_standings(code)
        
        if not valid_teams:
            print(f"  ⚠ Could not fetch standings, will use all teams from matches")
        else:
            print(f"  ✓ Found {len(valid_teams)} teams in current season")
        
        # Fetch matches for 2024 season
        print(f"  Fetching 2024 season matches...")
        matches_data = fetch_matches(code, "2024")
        
        if not matches_data:
            print(f"  ⚠ No matches fetched")
            continue
        
        print(f"  ✓ Fetched {len(matches_data)} matches")
        
        # Create league
        league = League(name=league_name, country=country, season="2024")
        session.add(league)
        session.flush()
        
        matches_imported = 0
        teams_created = 0
        teams_cache = {}
        
        for match_data in matches_data:
            try:
                home_team_name = match_data.get("homeTeam", {}).get("name")
                away_team_name = match_data.get("awayTeam", {}).get("name")
                
                if not home_team_name or not away_team_name:
                    continue
                
                # If we have valid teams list, only import matches with those teams
                if valid_teams:
                    if home_team_name not in valid_teams or away_team_name not in valid_teams:
                        continue
                
                # Get or create home team
                if home_team_name not in teams_cache:
                    home_team = Team(name=home_team_name, league_id=league.id)
                    session.add(home_team)
                    session.flush()
                    teams_cache[home_team_name] = home_team
                    teams_created += 1
                else:
                    home_team = teams_cache[home_team_name]
                
                # Get or create away team
                if away_team_name not in teams_cache:
                    away_team = Team(name=away_team_name, league_id=league.id)
                    session.add(away_team)
                    session.flush()
                    teams_cache[away_team_name] = away_team
                    teams_created += 1
                else:
                    away_team = teams_cache[away_team_name]
                
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
                    "PAUSED": "live",
                    "POSTPONED": "scheduled",
                    "SUSPENDED": "scheduled",
                    "CANCELLED": "scheduled"
                }
                status = status_map.get(match_data.get("status"), "scheduled")
                
                # Create match
                match = Match(
                    date=match_date,
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    league_id=league.id,
                    home_goals=home_goals,
                    away_goals=away_goals,
                    status=status,
                    round=match_data.get("matchday"),
                    referee=match_data.get("referees", [{}])[0].get("name") if match_data.get("referees") else None
                )
                session.add(match)
                matches_imported += 1
            
            except Exception as e:
                print(f"  Error processing match: {e}")
                continue
        
        session.commit()
        print(f"\n  ✓ Imported {matches_imported} matches")
        print(f"  ✓ Created {teams_created} teams")
        
        total_matches += matches_imported
        total_teams += teams_created
    
    session.close()
    
    print("\n" + "="*70)
    print(f"✓ IMPORT COMPLETED!")
    print(f"  Total matches imported: {total_matches}")
    print(f"  Total teams created: {total_teams}")
    print("="*70 + "\n")


def show_summary():
    """Show summary of imported data."""
    print("\n" + "="*70)
    print("DATABASE SUMMARY")
    print("="*70 + "\n")
    
    session = get_session()
    
    leagues = session.query(League).all()
    
    for league in leagues:
        team_count = session.query(Team).filter_by(league_id=league.id).count()
        match_count = session.query(Match).filter_by(league_id=league.id).count()
        finished_count = session.query(Match).filter_by(
            league_id=league.id,
            status='finished'
        ).count()
        upcoming_count = session.query(Match).filter_by(
            league_id=league.id,
            status='scheduled'
        ).count()
        
        print(f"{league.name}:")
        print(f"  Teams: {team_count}")
        print(f"  Total Matches: {match_count}")
        print(f"  Finished: {finished_count}")
        print(f"  Upcoming: {upcoming_count}")
        print()
    
    session.close()


def main():
    """Main function."""
    print("\n" + "="*70)
    print("CLEAN AND REIMPORT WITH CORRECT DATA")
    print("="*70 + "\n")
    
    print("This will:")
    print("1. Clear ALL existing data")
    print("2. Import ONLY correct teams from 2024 season")
    print("3. Import all matches for those teams")
    print("\n⚠ WARNING: This will delete everything and start fresh!\n")
    
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("\nOperation cancelled.")
        return
    
    # Clear all data
    clear_all_data()
    
    # Import correct data
    import_correct_data()
    
    # Show summary
    show_summary()
    
    print("\n" + "="*70)
    print("✓ PROCESS COMPLETED!")
    print("="*70)
    print("\nNext steps:")
    print("1. Train models: python scripts/train_all_models.py")
    print("2. Run app: python run.py")
    print()


if __name__ == '__main__':
    main()


