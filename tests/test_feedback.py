# tests/test_feedback.py
def login_as_student(client):
    client.post(
        '/login',
        data={'username': 'student1', 'password': 'password123'},
        follow_redirects=True
    )

def test_submit_feedback_valid(client):
    """Positive: student submits valid feedback."""
    login_as_student(client)
    rv = client.post(
        '/feedback',
        data={'sensor_id': '1', 'rating': 'hot', 'comment': 'Too warm'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'Thank you for your feedback!' in rv.data

def test_submit_feedback_invalid(client):
    """Negative: missing rating yields form error."""
    login_as_student(client)
    rv = client.post(
        '/feedback',
        data={'sensor_id': '1', 'rating': '', 'comment': 'Oops'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'This field is required' in rv.data
