"""
Observer pattern implementation for sensor status changes.
"""

from typing import List
from datetime import datetime

class SensorStatusObserver:
    def update(self, sensor_id: int, old_status: str, new_status: str):
        """
        Called when a sensor's status changes.
        """
        raise NotImplementedError

class SensorStatusSubject:
    """
    Subject that maintains a list of observers and notifies them of changes.
    """
    def __init__(self):
        self._observers: List[SensorStatusObserver] = []

    def attach(self, observer: SensorStatusObserver):
        """
        Add an observer to the notification list.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: SensorStatusObserver):
        """
        Remove an observer from the notification list.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, sensor_id: int, old_status: str, new_status: str):
        """
        Notify all observers about a status change.
        """
        for observer in self._observers:
            observer.update(sensor_id, old_status, new_status)

# Global subject instance to be used throughout the application
sensor_status_subject = SensorStatusSubject()


# -----------------------
# Dashboard notification
# -----------------------

# internal storage for dashboard events
_dashboard_notifications: List[dict] = []

class DashboardObserver(SensorStatusObserver):
    """
    Records each status change into an in-memory list for the dashboard.
    """
    def update(self, sensor_id: int, old_status: str, new_status: str):
        _dashboard_notifications.append({
            'sensor_id':   sensor_id,
            'old_status':  old_status,
            'new_status':  new_status,
            'timestamp':   datetime.utcnow()
        })

# attach our dashboard observer so it receives every update
_dashboard_observer = DashboardObserver()
sensor_status_subject.attach(_dashboard_observer)


def get_dashboard_notifications() -> List[dict]:
    """
    Return a copy of all recorded status-change notifications.
    Each dict has keys: sensor_id, old_status, new_status, timestamp.
    """
    return list(_dashboard_notifications)
