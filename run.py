"""
Entrypoint for running the Campus IoT Flask application.
"""

from app import create_app

app = create_app()  # Instantiate the Flask app via our factory

if __name__ == '__main__':
    # Enable debug mode during development for hot-reloading and better errors
    app.run(debug=True)
