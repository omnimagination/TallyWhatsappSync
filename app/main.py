"""
TallySync - Main Application Entry Point

Professional Desktop Application for TallyPrime Integration

Author: OmniMagination
Version: 1.0.0
"""

import sys
import os

# Add app directory to path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from app.core.config import config
from app.core.logger import logger
from app.ui.main_window import MainWindow


def main() -> None:
    """Main application entry point."""
    try:
        # Initialize logging
        logger.info("=" * 50, category="app")
        logger.info("TallySync v1.0.0 Starting...", category="app")
        logger.info("=" * 50, category="app")
        
        # Log configuration
        logger.info(f"Config loaded: {config._config_path}", category="app")
        logger.info(f"Database: {config.get_database_path()}", category="app")
        logger.info(f"Tally URL: {config.get_tally_url()}", category="app")
        
        # Create and run main window
        app = MainWindow()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user", category="app")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Application crashed: {e}", category="app", exc_info=True)
        print(f"\n? Critical Error: {e}")
        print("\nCheck logs folder for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
