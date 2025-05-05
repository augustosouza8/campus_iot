"""
Development utilities: reset and seed the database with sample data.
"""

from app import db
from app.models import Admin, Student, Sensor, Calibration, Feedback, TemperatureReading
import random
import datetime

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

    # --- Seed extra random feedback for demo ---
    extra_students = []
    for i in range(1, 21):
        student = Student(username=f'student{i+2}', email=f's{i+2}@campus.edu')
        student.set_password('password123')
        db.session.add(student)
        extra_students.append(student)
    db.session.commit()

    for idx, student in enumerate(extra_students):
        sensor = sensors[idx % len(sensors)]
        fb = Feedback(
            user_id=student.id,
            sensor_id=sensor.id,
            rating=random.choice(['hot', 'ok', 'cold']),
            comment='Auto-generated feedback'
        )
        db.session.add(fb)

    # --- Seed historical temperature readings (5 per sensor) ---
    now = datetime.datetime.utcnow()
    for sensor in sensors:
        # create 5 readings at 10‑minute intervals over the past 50 minutes
        for j in range(5):
            ts = now - datetime.timedelta(minutes=10 * j)
            temp = round(random.uniform(18.0, 26.0), 1)
            tr = TemperatureReading(
                sensor_id=sensor.id,
                timestamp=ts,
                temperature=temp
            )
            db.session.add(tr)
    db.session.commit()
    print("Database reset and seeded with sample data.")
