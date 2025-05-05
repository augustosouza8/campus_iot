"""
Dummy AI/ML module for analyzing sensors and feedback.
"""

import random
from typing import List
from app.models import Sensor, Feedback
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class OutdoorCondition:
    timestamp: datetime
    temp: float       # °C
    humidity: float   # % RH
    code: str         # e.g. 'Sunny', 'Cloudy'

def get_demo_outdoor_data():
    """
    Return a fixed list of hourly outdoor readings for demo purposes.
    """
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    # build 6 hours of past data plus current hour
    demo = []
    for hours_ago, (t, h, c) in enumerate([
        (15.2, 55, 'Cloudy'),
        (14.8, 57, 'Cloudy'),
        (14.5, 60, 'Partly Cloudy'),
        (14.0, 62, 'Sunny'),
        (13.7, 65, 'Sunny'),
        (13.5, 67, 'Fog'),
    ]):
        demo.append(
            OutdoorCondition(
                timestamp=now - timedelta(hours=5 - hours_ago),
                temp=t,
                humidity=h,
                code=c
            )
        )
    return demo

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



# Comfortable temperature range in °C for campus buildings
ACCEPTABLE_LOW = 20.0
ACCEPTABLE_HIGH = 24.0

# --- Simulate live sensor temperatures (helper for analytics/testing) ---
def simulate_live_temperatures(sensors):
    """
    Simulate a live temperature reading for each sensor.
    Returns a dict mapping sensor.id to a random temperature (°C).
    """
    # Simulate each sensor's temperature in a plausible range
    temps = {}
    for s in sensors:
        # Simulate a temperature between 18 and 26 °C
        temps[s.id] = round(random.uniform(18, 26), 1)
    return temps


def suggest_thermostat_adjustments(sensors, feedbacks, live_temps):
    """
    Generate dummy thermostat adjustment suggestions based on live temps and feedback.
    For each sensor/location:
      - If temp > ACCEPTABLE_HIGH or more 'hot' feedbacks, suggest lowering target by 1°C.
      - If temp < ACCEPTABLE_LOW or more 'cold' feedbacks, suggest raising target by 1°C.
      - Otherwise, report settings are OK.
    Returns a dict mapping sensor.location to suggestion string.
    """
    # Build feedback counts per sensor
    feedback_counts = {s.id: {'hot': 0, 'ok': 0, 'cold': 0} for s in sensors}
    for fb in feedbacks:
        if fb.sensor_id in feedback_counts:
            feedback_counts[fb.sensor_id][fb.rating] += 1

    suggestions = {}
    for sensor in sensors:
        loc = sensor.location
        temp = live_temps.get(sensor.id, None)
        counts = feedback_counts.get(sensor.id, {})
        hot = counts.get('hot', 0)
        cold = counts.get('cold', 0)

        if temp is not None and (temp > ACCEPTABLE_HIGH or hot > cold):
            suggestions[loc] = f"Current temp {temp}°C; consider lowering thermostat by 1°C."
        elif temp is not None and (temp < ACCEPTABLE_LOW or cold > hot):
            suggestions[loc] = f"Current temp {temp}°C; consider raising thermostat by 1°C."
        else:
            suggestions[loc] = f"Current temp {temp}°C; settings are within the comfortable range."

    return suggestions

@dataclass
class SensorFeatureVector:
    sensor_id: int
    location: str
    timestamp: datetime
    current_temp: float
    avg_temp_1h: float
    hot_feedback_count: int
    cold_feedback_count: int
    ok_feedback_count: int
    total_feedback_count: int
    outdoor_temp: float = None
    outdoor_humidity: float = None
    weather_code: str = None

def aggregate_sensor_features(sensors, feedbacks, live_temps, historical_temps, outdoor_data=None):
    """
    Build feature vectors for each sensor to feed into AI/ML model.

    - sensors: list of Sensor objects
    - feedbacks: list of Feedback objects
    - live_temps: dict sensor.id -> current temp
    - historical_temps: dict sensor.id -> list of (timestamp, temp)
    - outdoor_data: list of objects with attributes (timestamp, temp, humidity, code)

    Returns: list of SensorFeatureVector
    """
    # Count feedback by rating per sensor
    fb_counts = {s.id: {'hot':0,'ok':0,'cold':0} for s in sensors}
    for fb in feedbacks:
        if fb.sensor_id in fb_counts:
            fb_counts[fb.sensor_id][fb.rating] += 1

    # Compute 1h average temperature
    cutoff = datetime.utcnow().timestamp() - 3600
    avg_1h = {}
    for sid, readings in historical_temps.items():
        recent = [temp for ts, temp in readings if ts.timestamp() >= cutoff]
        avg_1h[sid] = sum(recent)/len(recent) if recent else live_temps.get(sid, 0)

    # Optionally index latest outdoor data
    latest_out = None
    if outdoor_data:
        latest_out = sorted(outdoor_data, key=lambda o: o.timestamp)[-1]

    # Build feature vectors
    now = datetime.utcnow()
    feature_list = []
    for s in sensors:
        sid = s.id
        cf = fb_counts.get(sid, {})
        vec = SensorFeatureVector(
            sensor_id=sid,
            location=s.location,
            timestamp=now,
            current_temp=live_temps.get(sid),
            avg_temp_1h=avg_1h.get(sid),
            hot_feedback_count=cf.get('hot',0),
            cold_feedback_count=cf.get('cold',0),
            ok_feedback_count=cf.get('ok',0),
            total_feedback_count=sum(cf.values()),
            outdoor_temp=(latest_out.temp if latest_out else None),
            outdoor_humidity=(latest_out.humidity if latest_out else None),
            weather_code=(latest_out.code if latest_out else None)
        )
        feature_list.append(vec)
    return feature_list