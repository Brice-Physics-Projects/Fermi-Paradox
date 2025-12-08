"""src/fermi_paradox/__init__.py"""

from flask import Flask
from flask_talisman import Talisman
from fermi_paradox.config.settings import get_config, logger

def create_app(config_class=None):
    """Application factory for Fermi Paradox Flask app."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Determine and load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        config_class = get_config()
        app.config.from_object(config_class)

    # Log environment mode
    logger.info(f"Starting Fermi Paradox app in {app.config.get('FLASK_ENV', 'development')} mode")

    # -----------------------------------------------------------
    # SECURITY HEADERS FOR SSL A/A+ RATING
    # -----------------------------------------------------------

    # Minimal default Content Security Policy
    csp = {
        "default-src": [
            "'self'"
        ]
    }

    # Add security headers via Flask-Talisman
    Talisman(
        app,
        content_security_policy=csp,
        force_https=True,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,   # 1 year (A+ requirement)
        strict_transport_security_include_subdomains=True,
        strict_transport_security_preload=True,
    )

    # -----------------------------------------------------------
    
    # Register blueprints
    from fermi_paradox.api.routes import api_bp
    app.register_blueprint(api_bp)

    return app
