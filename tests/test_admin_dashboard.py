# tests/test_admin_dashboard.py
def login_as(username, client):
    client.post(
        '/login',
        data={'username': username, 'password': 'password123'},
        follow_redirects=True
    )

def test_admin_dashboard_access(client):
    """Positive: admin sees dashboard and dummy AI summaries."""
    login_as('admin1', client)
    rv = client.get('/admin')
    assert rv.status_code == 200
    assert b'Admin Dashboard' in rv.data

def test_admin_dashboard_forbidden(client):
    """Negative: student is not allowed to view admin dashboard."""
    login_as('student1', client)
    rv = client.get('/admin')
    assert rv.status_code == 403
