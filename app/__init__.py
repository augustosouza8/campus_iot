"""
Application factory and extension initialization for Campus IoT app.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instantiate extensions
db = SQLAlchemy()
login = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # type: ignore

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'login'

    @app.shell_context_processor
    def make_shell_context():
        from app.models import User, Admin, Student, Sensor, Calibration, Feedback
        from app.debug_utils import reset_db
        return {
            'db': db,
            'User': User,
            'Admin': Admin,
            'Student': Student,
            'Sensor': Sensor,
            'Calibration': Calibration,
            'Feedback': Feedback,
            'reset_db': reset_db
        }

    from app.views import bp as main_bp
    app.register_blueprint(main_bp)
    return app
