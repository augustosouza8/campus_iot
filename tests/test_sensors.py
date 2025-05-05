# tests/test_sensors.py
from flask import url_for

def login_as_admin(client):
    client.post(
        '/login',
        data={'username': 'admin1', 'password': 'password123'},
        follow_redirects=True
    )

def test_add_sensor_valid(client):
    """Positive: admin can add a new sensor."""
    login_as_admin(client)
    rv = client.post(
        '/sensors',
        data={'name': 'Test Sensor', 'location': 'Lab 42', 'status': 'online'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'Sensor added successfully.' in rv.data
    assert b'Test Sensor' in rv.data

def test_add_sensor_invalid(client):
    """Negative: missing name yields form error."""
    login_as_admin(client)
    rv = client.post(
        '/sensors',
        data={'name': '', 'location': 'Lab 42', 'status': 'online'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'This field is required' in rv.data

def test_remove_sensor_valid(client):
    """Positive: admin can remove an existing sensor."""
    login_as_admin(client)
    # seeded sensor with id=1 ("Sensor A1")
    rv = client.post(
        '/sensors/remove',
        data={'record_id': '1'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'Sensor removed.' in rv.data
    assert b'Sensor A1' not in rv.data

def test_remove_sensor_invalid(client):
    """Negative: removing non-existent sensor does nothing."""
    login_as_admin(client)
    rv = client.post(
        '/sensors/remove',
        data={'record_id': '999'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    # seeded sensors still present
    assert b'Sensor A1' in rv.data

def test_toggle_sensor_status_valid(client):
    """Positive: admin can toggle status from offline→online."""
    login_as_admin(client)
    # seeded sensor id=2 is offline
    rv = client.post(
        '/sensors/toggle_status',
        data={'record_id': '2'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'Sensor status changed to online.' in rv.data
    assert b'Online' in rv.data

def test_toggle_sensor_status_invalid(client):
    """Negative: toggling non-existent sensor is a no-op."""
    login_as_admin(client)
    rv = client.post(
        '/sensors/toggle_status',
        data={'record_id': '999'},
        follow_redirects=True
    )
    assert rv.status_code == 200

def test_calibrate_sensor_valid(client):
    """Positive: admin can record a calibration."""
    login_as_admin(client)
    rv = client.post(
        '/sensors/calibrate',
        data={'sensor_id': '1', 'notes': 'Routine check'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'Calibration recorded.' in rv.data
    # sensor_detail page shows the note
    assert b'Routine check' in rv.data

def test_calibrate_sensor_unauthorized(client):
    """Negative: student cannot calibrate."""
    # log in as student
    client.post(
        '/login',
        data={'username': 'student1', 'password': 'password123'},
        follow_redirects=True
    )
    rv = client.post(
        '/sensors/calibrate',
        data={'sensor_id': '1', 'notes': 'Bad access'},
        follow_redirects=True
    )
    assert rv.status_code == 403
