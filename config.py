import os

class Config:
    """
    Base configuration for the Campus IoT Management app.

    Attributes:
        SECRET_KEY: Used by Flask (and Flask-WTF) to secure sessions and CSRF.
        SQLALCHEMY_DATABASE_URI: Path to the SQLite DB file.
        UPLOAD_FOLDER: Directory where uploaded files (if any) will be stored.
        MAX_CONTENT_LENGTH: Maximum size (in bytes) for incoming request bodies.
    """
    # Use an environment variable if set, else fallback to a static string.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # SQLAlchemy DB URI: store the SQLite file under app/data/data.sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app/data/data.sqlite'

    # Where to save uploaded files (we’ll create this folder next phase)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'data', 'uploads')

    # Limit uploads to 16 MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
