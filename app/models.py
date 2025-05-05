"""
SQLAlchemy ORM models with single-table inheritance for User subclasses.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

from app.observer import sensor_status_subject


class User(UserMixin, db.Model):
    """
    Base user class with polymorphic single-table inheritance.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    # Configure single-table inheritance
    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

    # Relationships
    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Admin(User):
    """
    Administrator user type.
    """
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __init__(self, username: str, email: str):
        # Set up Admin-specific defaults
        self.username = username
        self.email = email
        self.role = 'admin'


class Student(User):
    """
    Student user type.
    """
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.role = 'student'


@login.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    calibrations = db.relationship('Calibration', backref='sensor', cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='sensor', cascade='all, delete-orphan')

    readings = db.relationship(
        'TemperatureReading',
        back_populates='sensor',
        cascade='all, delete-orphan',
        order_by='TemperatureReading.timestamp'
    )

    def __repr__(self):
        return f'<Sensor {self.name} at {self.location}>'

    def set_status(self, new_status: str):
        """
        Set the sensor status and notify observers of the change.
        """
        if self.status != new_status:
            old_status = self.status
            self.status = new_status
            sensor_status_subject.notify(self.id, old_status, new_status)


class TemperatureReading(db.Model):
    __tablename__ = 'temperature_readings'

    id          = db.Column(db.Integer, primary_key=True)
    sensor_id   = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    temperature = db.Column(db.Float, nullable=False)

    sensor = db.relationship('Sensor', back_populates='readings')
class Calibration(db.Model):
    __tablename__ = 'calibrations'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    calibrated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        ts = self.calibrated_at.strftime('%Y-%m-%d %H:%M:%S')
        return f'<Calibration sensor={self.sensor_id} at {ts}>'


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        ts = self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        return f'<Feedback {self.rating} by User {self.user_id} at {ts}>'
