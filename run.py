"""Entry point for Fermi Paradox Flask app"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.fermi_paradox import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5000)
