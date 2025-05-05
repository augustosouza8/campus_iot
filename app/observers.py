"""
Example observers for the sensor status changes.
"""
from app.observer import SensorStatusObserver
from app.models import db, Sensor
from datetime import datetime

class StatusChangeLogger(SensorStatusObserver):
    """
    Logs all sensor status changes to the console.
    """
    def update(self, sensor_id: int, old_status: str, new_status: str):
        print(f"Sensor {sensor_id} changed from {old_status} to {new_status}")

class MaintenanceNotifier(SensorStatusObserver):
    """
    Sends notifications when sensors go offline.
    """
    def update(self, sensor_id: int, old_status: str, new_status: str):
        if new_status == 'offline':
            sensor = db.session.get(Sensor, sensor_id)
            print(f"ALERT: Sensor {sensor.name} at {sensor.location} is now offline!")

class CalibrationScheduler(SensorStatusObserver):
    """
    Schedules calibration when sensors come back online.
    """
    def update(self, sensor_id: int, old_status: str, new_status: str):
        if old_status == 'offline' and new_status == 'online':
            sensor = db.session.get(Sensor, sensor_id)
            print(f"Scheduling calibration for sensor {sensor.name}")

# Register the observers when the module loads
from app.observer import sensor_status_subject
sensor_status_subject.attach(StatusChangeLogger())
sensor_status_subject.attach(MaintenanceNotifier())
sensor_status_subject.attach(CalibrationScheduler())