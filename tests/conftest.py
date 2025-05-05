# tests/conftest.py
import os
import pytest

import config
# force in-memory database for tests before create_app reads it
config.Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

from app import create_app, db
from app.debug_utils import reset_db

@pytest.fixture
def app():
    # create the Flask app with testing config
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,       # disable CSRF for form posts in tests
    })

    with app.app_context():
        # reset_db drops/creates tables and seeds sample data
        reset_db()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
