"""
Configuration settings for Fermi Paradox Flask app.

src/fermi_paradox/config/settings.py
"""

import os
import logging
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env (if present)
load_dotenv(find_dotenv())

# -----------------------------------------------------------------------------
# Configuration Classes
# -----------------------------------------------------------------------------

class Config:
    """Base configuration shared by all environments."""

    # Corrected variable name: use SECRET_KEY (no space)
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # Common Flask settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_RELOADER = False

    # Logging level can be overridden by env var
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = "development"
    USE_RELOADER = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # Avoid pausing form submissions


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = "production"


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    FLASK_ENV = "testing"
    DEBUG = False


# -----------------------------------------------------------------------------
# Logger Setup
# -----------------------------------------------------------------------------

logger = logging.getLogger("fermi_paradox")
logger.setLevel(getattr(logging, os.getenv("LOG_LEVEL", "DEBUG").upper()))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Format: timestamp - module - level - message
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.handlers:
    logger.addHandler(console_handler)

# -----------------------------------------------------------------------------
# Helper: Environment-Aware Config Selector
# -----------------------------------------------------------------------------

def get_config():
    """Return the appropriate config class based on FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    return DevelopmentConfig
