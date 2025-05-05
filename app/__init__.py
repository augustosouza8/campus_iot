"""
Application factory and extension initialization for Campus IoT app. Hello
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instantiate extensions at module scope
db = SQLAlchemy()  # Database ORM
login = LoginManager()  # Login/session manager


def create_app():
    """
    Create and configure the Flask application.

    - Loads configuration from config.Config
    - Initializes extensions (SQLAlchemy, LoginManager)
    - Registers shell context so you can `flask shell` and have db & models pre-imported
    - Imports views so that routes are registered
    """
    app = Flask(__name__)

    # Load settings from config.py
    app.config.from_object('config.Config')  # type: ignore

    # Initialize Flask extensions with the app
    db.init_app(app)
    login.init_app(app)

    # Redirect unauthorized users to the login page
    login.login_view = 'login'

    # Shell context for `flask shell` (optional but handy)
    @app.shell_context_processor
    def make_shell_context():
        from app.models import User, Sensor, Calibration, Feedback
        from app.debug_utils import reset_db
        return {
            'db': db,
            'User': User,
            'Sensor': Sensor,
            'Calibration': Calibration,
            'Feedback': Feedback,
            'reset_db': reset_db
        }



    # # Import routes and error handlers so they’re registered
    # from app import views  # noqa: E402
    #
    # return app


    # Import and register our view‐blueprint
    from app.views import bp as main_bp  # blueprint defined below
    from app import observers
    app.register_blueprint(main_bp)

    return app

