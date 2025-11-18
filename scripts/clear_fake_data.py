"""Script to remove simulated/fake data and keep only real imported data."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from database.connection import get_session, init_db
from models.database import League, Team, Match, MatchStats, Prediction, UserBet
from datetime import datetime


def clear_fake_data():
    """Remove simulated data, keep only real imported data."""
    print("\n" + "="*70)
    print("REMOVING SIMULATED/FAKE DATA")
    print("="*70 + "\n")
    
    init_db()
    session = get_session()
    
    try:
        # Real team names from the 5 major leagues we imported
        real_leagues = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
        
        # Get real leagues
        real_league_ids = []
        for league_name in real_leagues:
            league = session.query(League).filter_by(name=league_name).first()
            if league:
                real_league_ids.append(league.id)
        
        print(f"Found {len(real_league_ids)} real leagues to keep\n")
        
        # Delete predictions for fake matches
        print("Clearing old predictions...")
        deleted_predictions = session.query(Prediction).delete()
        print(f"  ✓ Deleted {deleted_predictions} old predictions\n")
        
        # Delete user bets
        print("Clearing user bets...")
        deleted_bets = session.query(UserBet).delete()
        print(f"  ✓ Deleted {deleted_bets} user bets\n")
        
        # Delete match stats for fake matches
        print("Clearing match statistics...")
        deleted_stats = session.query(MatchStats).delete()
        print(f"  ✓ Deleted {deleted_stats} match statistics\n")
        
        # Delete matches from fake leagues
        print("Removing matches from simulated leagues...")
        fake_matches = session.query(Match).filter(
            ~Match.league_id.in_(real_league_ids)
        ).delete(synchronize_session=False)
        print(f"  ✓ Deleted {fake_matches} fake matches\n")
        
        # Delete teams from fake leagues
        print("Removing teams from simulated leagues...")
        fake_teams = session.query(Team).filter(
            ~Team.league_id.in_(real_league_ids)
        ).delete(synchronize_session=False)
        print(f"  ✓ Deleted {fake_teams} fake teams\n")
        
        # Delete fake leagues
        print("Removing simulated leagues...")
        fake_leagues = session.query(League).filter(
            ~League.id.in_(real_league_ids)
        ).delete(synchronize_session=False)
        print(f"  ✓ Deleted {fake_leagues} fake leagues\n")
        
        session.commit()
        
        # Show what's left
        print("="*70)
        print("REMAINING DATA (REAL ONLY)")
        print("="*70 + "\n")
        
        remaining_leagues = session.query(League).count()
        remaining_teams = session.query(Team).count()
        remaining_matches = session.query(Match).count()
        
        print(f"Leagues: {remaining_leagues}")
        print(f"Teams: {remaining_teams}")
        print(f"Matches: {remaining_matches}")
        
        # Show breakdown by league
        print("\nBreakdown by league:")
        for league in session.query(League).all():
            team_count = session.query(Team).filter_by(league_id=league.id).count()
            match_count = session.query(Match).filter_by(league_id=league.id).count()
            print(f"  {league.name}: {team_count} teams, {match_count} matches")
        
        print("\n" + "="*70)
        print("✓ CLEANUP COMPLETED!")
        print("="*70)
        print("\nYour database now contains ONLY real football data!")
        print("All simulated/fake data has been removed.\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    print("\n⚠ WARNING: This will DELETE all simulated/fake data.")
    print("Only real imported data from the 5 major leagues will remain.\n")
    
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        clear_fake_data()
    else:
        print("\nCleanup cancelled.")


