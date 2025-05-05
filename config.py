import os

# Compute the project base directory (where config.py lives)
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Build an absolute path to app/data/data.sqlite
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' +
        os.path.join(BASEDIR, 'app', 'data', 'data.sqlite')
    )

    # (Optional but recommended)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASEDIR, 'app', 'data', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
