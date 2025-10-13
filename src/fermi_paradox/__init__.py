"""src/fermi_paradox/__init__.py"""

from flask import Flask
from fermi_paradox.config.settings import get_config, logger
import os

def create_app(config_class=None):
    """Application factory pattern for Fermi Paradox Flask app."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    logger.info(f"Starting Fermi Paradox app in {env} mode")

    # Register blueprints
    from fermi_paradox.api.routes import api_bp
    app.register_blueprint(api_bp)

    # Optional: initialize database or extensions here later
    # db.init_app(app)
    # migrate.init_app(app, db)

    return app
