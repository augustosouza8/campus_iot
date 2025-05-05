"""
SQLAlchemy ORM models for the Campus IoT Management app.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login  # import the db and login extensions


class User(UserMixin, db.Model):
    """
    User of the system. Can be an 'admin' or 'student'.
    Inherits UserMixin so Flask-Login knows how to handle session stuff.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # unique PK
    username = db.Column(db.String(64), unique=True, nullable=False)  # login name
    email = db.Column(db.String(120), unique=True, nullable=False)    # contact info
    password_hash = db.Column(db.String(128), nullable=False)         # hashed password
    role = db.Column(db.String(20), nullable=False)                  # 'admin' or 'student'

    # One-to-many relationships: a user can submit many feedbacks
    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hash & store the password."""
        self.password_hash = generate_password_hash(password)  # werkzeug helper

    def check_password(self, password: str) -> bool:
        """Verify the password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


@login.user_loader
def load_user(user_id: str):
    """
    Flask-Login callback to reload user object from the user ID stored in session.
    """
    return User.query.get(int(user_id))


class Sensor(db.Model):
    """
    Represents a fake/dummy IoT sensor installed in a campus room.
    """
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)       # e.g. "Sensor A1"
    location = db.Column(db.String(128), nullable=False)  # e.g. "Building 1, Room 101"
    status = db.Column(db.String(20), nullable=False)     # e.g. "online", "offline"

    # A sensor can have many calibration events
    calibrations = db.relationship('Calibration', backref='sensor', cascade='all, delete-orphan')
    # A sensor can receive many student feedbacks
    feedbacks = db.relationship('Feedback', backref='sensor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Sensor {self.name} at {self.location}>'


class Calibration(db.Model):
    """
    Records each time an admin calibrates a sensor.
    """
    __tablename__ = 'calibrations'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    calibrated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text, nullable=True)  # optional description of calibration

    def __repr__(self):
        ts = self.calibrated_at.strftime('%Y-%m-%d %H:%M:%S')
        return f'<Calibration sensor={self.sensor_id} at {ts}>'


class Feedback(db.Model):
    """
    Student-submitted temperature feedback for a sensor (room).
    """
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    rating = db.Column(db.String(10), nullable=False)     # e.g. 'hot', 'ok', 'cold'
    comment = db.Column(db.Text, nullable=True)           # optional student comment
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        ts = self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        return f'<Feedback {self.rating} by User {self.user_id} at {ts}>'
