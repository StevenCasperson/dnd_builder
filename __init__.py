
# dnd_builder/__init__.py
# ----------------------
# This file initializes the dnd_builder package and sets up the Flask app factory, database, and blueprints.
# Each section and function is now commented for clarity and maintainability.

import os  # Standard library for interacting with the operating system

from flask import Flask  # Import Flask class for creating the app
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy extension for database support

db = SQLAlchemy()  # Create a package-level SQLAlchemy extension instance (used for database access throughout the app)

def create_app():  # Factory function to create and configure the Flask app
    project_root = os.path.abspath(  # Determine the absolute path to the project root (one level up from this file)
        os.path.join(os.path.dirname(__file__), os.pardir)
    )

    app = Flask(  # Create the Flask app, specifying the root-level templates and static folders
        __name__,
        template_folder=os.path.join(project_root, "templates"),  # Set the template folder
        static_folder=os.path.join(project_root, "static")        # Set the static folder
    )

    app.jinja_env.globals['getattr']   = getattr  # Make Python's getattr function available in Jinja templates for dynamic attribute access
    app.jinja_env.globals['attribute'] = getattr  # Alias for getattr in Jinja

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-replace-me")  # Secret key for session security
    app.config["SQLALCHEMY_DATABASE_URI"] = (  # Database URI for SQLAlchemy
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(project_root, 'dnd_builder.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable event system for performance

    db.init_app(app)  # Initialize Flask extensions (e.g., SQLAlchemy)

    from .characters import bp as characters_bp  # Import the characters blueprint
    from .encounters import bp as encounter_bp   # Import the encounters blueprint
    from .download   import bp as download_bp    # Import the download blueprint

    app.register_blueprint(characters_bp, url_prefix="/characters")  # Register blueprint for character creation and management
    app.register_blueprint(encounter_bp, url_prefix="/inn")          # Register blueprint for encounters and adventure logic
    app.register_blueprint(download_bp,  url_prefix="/download")     # Register blueprint for PDF and data download endpoints

    @app.template_filter("format_coins")  # Add a custom Jinja filter for formatting coin dictionaries in templates
    def format_coins_filter(coins: dict) -> str:
        parts = []  # List to hold formatted coin strings
        for denom in ("pp", "gp", "sp", "cp"):  # Iterate over coin denominations in order
            count = coins.get(denom, 0)  # Get the count for this denomination
            if count:  # If there are coins of this type
                parts.append(f"{count} {denom}")  # Add formatted string to list
        return ", ".join(parts) or "0 cp"  # Join all parts or return '0 cp' if empty

    return app  # Return the configured Flask app instance
