"""
Main entry point for the Wordle solver application.
"""

import os
from web_interface.app import app
import config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def setup_data_directory():
    """Create the data directory if it doesn't exist."""
    os.makedirs(config.DATA_DIR, exist_ok=True)


def main():
    """Main entry point for the application."""
    # Ensure data directory exists
    setup_data_directory()

    # Start the web server with hot-reloading enabled
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
        use_reloader=True,  # Enable hot-reloading
        threaded=True  # Enable threading for better performance
    )


if __name__ == '__main__':
    main()
