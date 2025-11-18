"""Script to check if the application is properly set up."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def check_dependencies():
    """Check if all required packages are installed."""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    required_packages = [
        'customtkinter',
        'sqlalchemy',
        'sklearn',
        'xgboost',
        'lightgbm',
        'pandas',
        'numpy',
        'pydantic'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All dependencies installed!")
        return True


def check_database():
    """Check if database exists and has data."""
    print("\n" + "="*60)
    print("CHECKING DATABASE")
    print("="*60)
    
    try:
        from database.connection import get_session, init_db
        from models.database import League, Team, Match
        
        # Initialize database
        init_db()
        
        session = get_session()
        
        # Check for data
        leagues_count = session.query(League).count()
        teams_count = session.query(Team).count()
        matches_count = session.query(Match).count()
        
        print(f"Leagues: {leagues_count}")
        print(f"Teams: {teams_count}")
        print(f"Matches: {matches_count}")
        
        if leagues_count == 0 or teams_count == 0 or matches_count == 0:
            print("\n⚠ Database is empty or incomplete")
            print("Run: python scripts/seed_database.py")
            return False
        else:
            print("\n✓ Database is properly seeded!")
            return True
    
    except Exception as e:
        print(f"\n✗ Database error: {e}")
        print("Run: python scripts/seed_database.py")
        return False


def check_models():
    """Check if ML models are trained and available."""
    print("\n" + "="*60)
    print("CHECKING ML MODELS")
    print("="*60)
    
    try:
        from utils.config import Config
        
        model_files = [
            'xgboost_1x2.pkl',
            'lgbm_1x2.pkl',
            'rf_1x2.pkl',
            'xgboost_btts.pkl',
            'rf_ou25.pkl'
        ]
        
        missing = []
        
        for model_file in model_files:
            model_path = os.path.join(Config.ML_MODELS_DIR, model_file)
            if os.path.exists(model_path):
                print(f"✓ {model_file}")
            else:
                print(f"✗ {model_file} - NOT FOUND")
                missing.append(model_file)
        
        if missing:
            print(f"\n⚠ Missing models: {', '.join(missing)}")
            print("Run: python scripts/train_all_models.py")
            return False
        else:
            print("\n✓ All models are trained!")
            return True
    
    except Exception as e:
        print(f"\n✗ Error checking models: {e}")
        return False


def main():
    """Main check function."""
    print("\n" + "="*60)
    print("FOOTBALL PREDICTOR PRO - SETUP CHECK")
    print("="*60)
    
    deps_ok = check_dependencies()
    db_ok = check_database()
    models_ok = check_models()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if deps_ok and db_ok and models_ok:
        print("\n✓ Everything is set up correctly!")
        print("\nYou can now run the application:")
        print("  python run.py")
        print("\nOr:")
        print("  python src/main.py")
    else:
        print("\n⚠ Setup incomplete. Please follow these steps:\n")
        
        if not deps_ok:
            print("1. Install dependencies:")
            print("   pip install -r requirements.txt\n")
        
        if not db_ok:
            print("2. Seed the database:")
            print("   python scripts/seed_database.py\n")
        
        if not models_ok:
            print("3. Train ML models:")
            print("   python scripts/train_all_models.py\n")
        
        print("Then run this check again:")
        print("  python scripts/check_setup.py")
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()



