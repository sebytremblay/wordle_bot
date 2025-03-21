"""
Main entry point for the Wordle solver application.
"""

import os
from web_interface.app import app
import config


def setup_data_directory():
    """Create the data directory if it doesn't exist."""
    os.makedirs(config.DATA_DIR, exist_ok=True)


def main():
    """Main entry point for the application."""
    # Ensure data directory exists
    setup_data_directory()

    # Start the web server
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
