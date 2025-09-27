# dnd_builder/encounters.py
# -------------------------
# This module defines the blueprint and routes for the 'inn' section of the app, which will handle encounters and adventure locations.
#
# Each section and function is now commented for clarity and maintainability.
#
# ——— Imports ———
from flask import Blueprint, render_template  # Import Flask Blueprint and template rendering

# Create a Flask Blueprint for encounter-related routes (the 'inn')
bp = Blueprint("encounter", __name__, url_prefix="/inn")  # All routes in this blueprint are prefixed with /inn

# Route for the inn landing page (main hub for encounters)
@bp.route("/")
def inn_landing():
    """
    Render the inn.html template (the main inn/adventure hub page).
    This is the landing page for the inn, where players can access encounters, locations, and adventure hooks.
    """
    return render_template("inn.html")  # Render the inn hub template

# … all your other /hearth, /bar, /board, etc. routes …
