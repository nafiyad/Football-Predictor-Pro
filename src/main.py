"""Main application entry point."""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from gui.app import FootballPredictorApp
from utils.config import Config
from utils.logger import setup_logger
from database.connection import init_db

# Setup logger
logger = setup_logger("main")


def main():
    """Main function to start the application."""
    try:
        # Ensure directories exist
        Config.ensure_directories()
        
        # Initialize database
        logger.info("Initializing database...")
        init_db()
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode(Config.DEFAULT_THEME)
        ctk.set_default_color_theme(Config.COLOR_THEME)
        
        logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
        
        # Create and run application
        app = FootballPredictorApp()
        app.mainloop()
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"\nError starting application: {e}")
        print("Please check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()



