# dnd_builder/models.py
# ---------------------
# This module defines the User model for authentication and user management.
# It uses SQLAlchemy for ORM and Werkzeug for password hashing.
#
# Each section and method is now commented for clarity and maintainability.
#
# ——— Imports ———
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing and checking
from .. import db  # Import the SQLAlchemy database instance
from ..models import User  # Import base User model (if using app factory pattern)

# UserMixin provides default implementations for Flask-Login user methods
class User(UserMixin, db.Model):
    # Unique integer ID for each user (primary key)
    id = db.Column(db.Integer, primary_key=True)
    # User's email address (must be unique and not null)
    email = db.Column(db.String(128), unique=True, nullable=False)
    # Hashed password (never store plaintext passwords)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """
        Hash and store the user's password using scrypt.
        This method takes a plaintext password, hashes it securely, and stores the hash.
        """
        self.password_hash = generate_password_hash(password, method="scrypt")

    def check_password(self, password):
        """
        Check a plaintext password against the stored hash.
        Returns True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
