import pytest
import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your Flask app
try:
    from run import app as flask_app
except ImportError:
    # Alternative import if run.py doesn't work
    try:
        from app import create_app
        flask_app = create_app()
    except ImportError:
        # Create a minimal Flask app for testing
        from flask import Flask
        flask_app = Flask(__name__)

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key"
    })
    
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()