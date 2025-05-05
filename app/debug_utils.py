"""
Development utilities: reset and seed the database with sample data.
"""

from app import db
from app.models import Admin, Student, Sensor, Calibration, Feedback


def reset_db():
    """
    Drop all tables, recreate schema, and seed with sample users, sensors,
    calibrations, and feedback entries.
    """
    # DROP & CREATE
    db.drop_all()
    db.create_all()

    # --- Seed Users ---
    admins = [
        Admin(username='admin1', email='admin1@campus.edu'),
        Admin(username='admin2', email='admin2@campus.edu'),
    ]
    students = [
        Student(username='student1', email='s1@campus.edu'),
        Student(username='student2', email='s2@campus.edu'),
    ]
    for u in admins + students:
        u.set_password('password123')

    db.session.add_all(admins + students)
    db.session.commit()

    # --- Seed Sensors ---
    sensors = [
        Sensor(name='Sensor A1', location='Building 1 - Room 101', status='online'),
        Sensor(name='Sensor B2', location='Building 2 - Room 202', status='offline'),
        Sensor(name='Sensor C3', location='Building 3 - Room 303', status='online'),
    ]
    db.session.add_all(sensors)
    db.session.commit()

    # --- Seed Calibrations ---
    calibrations = [
        Calibration(sensor_id=sensors[0].id, notes='Initial setup calibration'),
        Calibration(sensor_id=sensors[1].id, notes='Routine check'),
    ]
    db.session.add_all(calibrations)

    # --- Seed Feedback ---
    feedbacks = [
        Feedback(user_id=students[0].id, sensor_id=sensors[0].id, rating='ok', comment='Room feels fine'),
        Feedback(user_id=students[1].id, sensor_id=sensors[1].id, rating='hot', comment='Too warm today'),
    ]
    db.session.add_all(feedbacks)
    db.session.commit()
    print("Database reset and seeded with sample data.")
