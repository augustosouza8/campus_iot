# tests/test_auth.py
def test_login_success(client):
    """Positive: admin logs in with correct credentials."""
    rv = client.post(
        '/login',
        data={'username': 'admin1', 'password': 'password123'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'Logout admin1' in rv.data

def test_login_failure(client):
    """Negative: login fails with wrong password."""
    rv = client.post(
        '/login',
        data={'username': 'admin1', 'password': 'wrongpass'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b'Invalid username or password' in rv.data
