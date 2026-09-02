import sys
import os

# Ensure the project root is importable so `from app import create_app` works
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Vercel's Python runtime looks for a WSGI callable named `app`
app = create_app()
