"""
Observer pattern implementation for sensor status changes.
"""
from typing import List, Callable

class SensorStatusObserver:
    """
    Observer interface that concrete observers must implement.
    """
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