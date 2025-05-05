"""
Dummy AI/ML module for analyzing sensors and feedback.
"""

from typing import List
from app.models import Sensor, Feedback

def summarize_sensors(sensors: List[Sensor]) -> str:
    """
    Returns a simple summary of sensor status counts, tagged as a dummy AI result.
    """
    total = len(sensors)
    online = sum(s.status == 'online' for s in sensors)
    offline = sum(s.status == 'offline' for s in sensors)
    base = f"Total sensors: {total}; Online: {online}; Offline: {offline}"
    return f"[Dummy AI] {base}"


def summarize_feedback(feedbacks: List[Feedback]) -> str:
    """
    Returns a simple summary of feedback rating distribution, tagged as a dummy AI result.
    """
    total = len(feedbacks)
    hot = sum(fb.rating == 'hot' for fb in feedbacks)
    ok = sum(fb.rating == 'ok' for fb in feedbacks)
    cold = sum(fb.rating == 'cold' for fb in feedbacks)
    base = f"Total feedbacks: {total}; Hot: {hot}; OK: {ok}; Cold: {cold}"
    return f"[Dummy AI] {base}"
